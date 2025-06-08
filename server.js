const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const app = express();
const PORT = 1800;

// ミドルウェアの設定
app.use(cors());
app.use(express.json());
app.use(express.static('./'));

// すべてのリクエストをログに記録
app.use((req, res, next) => {
  const now = new Date();
  console.log(`[${now.toISOString()}] ${req.method} ${req.url}`);
  if (req.method === 'POST') {
    console.log('リクエストボディ:', JSON.stringify(req.body, null, 2));
  }
  next();
});

// GASへのPOSTリクエストをプロキシ
app.post('/proxy-gas', async (req, res) => {
  const GAS_URL = req.body.gasUrl || 'https://script.google.com/macros/s/AKfycbydPV0C9k_ZEnAaolxhJV00T6OC73vayf9PVWq7NZ4LhLqsRv9jbg0OIDYyTzQfaf9h/exec';
  const postData = req.body.data || {};
  
  console.log('GASへの送信:', GAS_URL);
  console.log('送信データ:', JSON.stringify(postData, null, 2));
  
  try {
    const response = await fetch(GAS_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(postData)
    });
    
    // GASからのレスポンスを取得
    const text = await response.text();
    console.log('GASからのレスポンス:', text);
    
    res.json({
      success: true,
      message: 'GASにデータを送信しました',
      response: text
    });
  } catch (error) {
    console.error('GAS送信エラー:', error);
    res.status(500).json({
      success: false,
      message: 'GASへの送信に失敗しました',
      error: error.message
    });
  }
});

// サーバーを起動
app.listen(PORT, () => {
  console.log(`サーバーが起動しました: http://localhost:${PORT}`);
  console.log(`診断フローにアクセスするには: http://localhost:${PORT}/diagnosis.html`);
  console.log(`Ctrl+C で終了します`);
}); 