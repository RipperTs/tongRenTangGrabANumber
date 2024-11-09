# 北京同仁堂抢号助手

## 部署

### 启动nodejs服务
因扣算法代码比较麻烦, 这里直接提供nodejs部署来生成算法了. 请确保你的服务器上有nodejs环墶

```shell
cd js && npm install && node index.js
```

### python执行抢号
- 修改  `JS_SERVICE_URL` 为你的nodejs服务地址
- 安装依赖 `pip install -r requirements.txt`
- 执行 `python main.py`