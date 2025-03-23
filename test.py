import requests

while True:
    query = input("\n请输入要查询的文本：")
    if query.lower() == 'q':
        break
        
    response = requests.post(
        "http://localhost:6006/search",
        json={"query": query, "top_k": 3}
    )
    
    results = response.json()["results"]
    print("\n最相似的文本：")
    for text_obj in results:
        print(f"相似度 {text_obj['score']:.4f}: {text_obj['text']}")