# Mnemosyne
一个快速、好用。且不消耗API key的AI记忆系统。


### 启动步骤



首先部署虚拟环境
```bash
conda create -n mnemosyne python=3.10 -y

conda activate mnemosyne
```


安装依赖
```bash
pip install -r requirements.txt

#安装cuda 默认是11.8 可以自行修改
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

启动文本嵌入模型服务

```bash
python rag-api.py
```
