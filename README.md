# 北京同仁堂中医医院抢号助手

> **北京同仁堂中医医院小程序专用**, 纯协议类似抢号.     
> 因在 [【富贵科技工作室派单群】](https://qm.qq.com/q/OwJdEv0Z8G) 接单各种理由不结算, 因此将此项目开源, 请勿用于商业用途, 仅供学习交流

## 使用
- 下载二进制文件运行, 目前Windows和MacOS已经打包好了, linux请自行打包
- `.env` 里面配置正确的参数, 其中 `JS_SERVICE_URL` 为nodejs服务地址, 其余的参数通过抓包得到
- 运行 `./qh -h` 查看帮助

## 部署

### 启动nodejs服务
因扣算法代码比较麻烦, 这里直接提供nodejs部署来生成算法了. 请确保你的服务器上有nodejs环墶

```shell
cd js && npm install && node index.js
```

### python执行抢号
- 修改  `JS_SERVICE_URL` 为你的nodejs服务地址
- 安装依赖 `pip install -r requirements.txt`
- 执行 `python main.py`, 支持 `-type` 参数

### 打包
```shell
pyinstaller -F main.py -n qh
```