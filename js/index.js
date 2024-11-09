const express = require('express');
const bodyParser = require('body-parser');
const n = require('./utils/sm4_index.js');
const sm3 = require('./utils/sm3_index.js');

const app = express();
const port = 13451;

// 使用中间件解析JSON请求体
app.use(bodyParser.json());

/**
 * 参数加密算法
 * @param requestData
 * @returns {string | []}
 */
function parameterEncryption(requestData) {
    let o = '3879696f4c6e5659522a3433266f2e33';
    return n.encrypt(requestData, o);
}

/**
 * 请求参数签名算法
 */
function getSignature(requestData, uuidStr) {
    let c = 'EvAucyQXqhNrXB23hw8wPw73xHzAHNqipmBFKJTHGzBXTsHpNxR9PGyMhErNEvAu';
    let a = uuidStr;
    let l = sm3(requestData);
    let p = a.substring(5);
    return sm3(c + a + p + l);
}

// 加密接口
app.post('/encrypt', (req, res) => {
    try {
        const { data } = req.body;
        if (!data) {
            return res.status(400).json({ error: 'Missing data parameter' });
        }

        const encrypted = parameterEncryption(JSON.stringify(data));
        res.json({ encrypted });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// 签名接口
app.post('/signature', (req, res) => {
    try {
        const { data, uuid } = req.body;
        if (!data || !uuid) {
            return res.status(400).json({ error: 'Missing required parameters' });
        }
        const signature = getSignature(JSON.stringify(data), uuid);
        res.json({ signature });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// 组合接口：同时返回加密和签名结果
app.post('/encrypt-and-sign', (req, res) => {
    try {
        const { data, uuid } = req.body;
        if (!data || !uuid) {
            return res.status(400).json({ error: 'Missing required parameters' });
        }
        const encrypted = parameterEncryption(data);
        const signature = getSignature(data, uuid);
        res.json({ encrypted, signature });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// 健康检查接口
app.get('/health', (req, res) => {
    res.json({ status: 'ok' });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});