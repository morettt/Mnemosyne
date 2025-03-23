# Mnemosyne
一个快速、好用。且不消耗API key的AI记忆系统。制作中...

首先，这是letta的记忆逻辑，我做了一个图来理解

![image](https://github.com/user-attachments/assets/c9c4be3b-982d-474b-b408-3e510a1e2723)



我的创新点是在letta的记忆逻辑上，将所有基于function calling的地方全都用bert或者小型开源的llm替代，大大减轻API KEY的消耗量，以及显著提升推理速度。


### 启动步骤



首先部署虚拟环境
```bash
conda create -n mnemosyne python=3.10 -y

#linex系统
source activate mnemosyne
#win系统
conda activate mnemosyne
```


安装依赖
```bash
pip install -r requirements.txt

#安装cuda 默认是11.8 可以自行修改
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

下载模型
```bash
modelscope download --model Xorbits/bge-large-zh-v1.5 --local_dir ./model/RAG

```

启动文本嵌入模型服务

```bash
python rag-api.py
```


最后运行此代码测试

```bash
python test.py
```


