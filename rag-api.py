from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Tuple, Optional
import numpy as np
import os
import uvicorn
from modelscope import snapshot_download
from FlagEmbedding import FlagModel
from contextlib import asynccontextmanager

# 请求和响应模型
class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

class TextSimilarity(BaseModel):
    text: str
    score: float

class QueryResponse(BaseModel):
    results: List[TextSimilarity]

# 全局变量
model = None
text_database = []

@asynccontextmanager
async def lifespan(api: FastAPI):
    # 启动时执行
    global model, text_database
    
    # 初始化模型
    model_dir = r'\model\RAG'
    model = FlagModel(
        model_dir,
        query_instruction_for_retrieval="检索：",
        use_fp16=True
    )
    
    # 读取文本数据库文件
    try:
        database_file = os.path.join(os.path.dirname(__file__), 'text_database.txt')
        with open(database_file, 'r', encoding='utf-8') as f:
            text_database = [line.strip() for line in f.readlines() if line.strip()]
        print(f"成功加载数据库，共{len(text_database)}条记录")
    except Exception as e:
        print(f"加载数据库失败: {str(e)}")
        text_database = []
    
    yield
    
    # 清理资源（如果需要）
    print("正在关闭应用...")

# 创建FastAPI实例
api = FastAPI(
    title="文本相似度搜索API",
    description="基于BGE模型的文本相似度搜索服务",
    version="1.0.0",
    lifespan=lifespan
)

# 相似度搜索函数
def find_similar_texts(query: str, database: List[str], top_k: int = 3) -> List[Tuple[str, float]]:
    if not database:
        return []
    
    # 编码查询文本
    query_embedding = model.encode_queries([query])
    
    # 编码数据库文本
    database_embeddings = model.encode(database)
    
    # 计算相似度
    similarities = query_embedding @ database_embeddings.T
    
    # 获取top_k个最相似的结果
    k = min(top_k, len(database))
    top_k_indices = np.argsort(similarities[0])[-k:][::-1]
    
    return [(database[i], float(similarities[0][i])) for i in top_k_indices]

# API路由
@api.post("/search", response_model=QueryResponse)
async def search(request: QueryRequest):
    if not model:
        raise HTTPException(status_code=503, detail="模型尚未加载完成")
    
    if not text_database:
        raise HTTPException(status_code=503, detail="文本数据库为空")
    
    results = find_similar_texts(request.query, text_database, request.top_k)
    
    return {
        "results": [
            {"text": text, "score": score} for text, score in results
        ]
    }

# 健康检查接口
@api.get("/health")
async def health_check():
    return {"status": "healthy", "database_size": len(text_database)}

# 启动服务器
if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=6006)
