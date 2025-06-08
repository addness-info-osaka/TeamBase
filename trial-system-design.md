# TeamBase 無料トライアル管理システム 設計書

## 📋 システム概要

14日間の無料トライアル期間を管理し、自動的な有料プランへの移行、請求処理を行うシステム

## 🔧 必要な機能

### 1. **トライアル期間管理**

#### データベース設計
```sql
-- 契約管理テーブル
CREATE TABLE contracts (
  id INT PRIMARY KEY AUTO_INCREMENT,
  company_name VARCHAR(255) NOT NULL,
  contact_name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  phone VARCHAR(50),
  department VARCHAR(255),
  employee_count VARCHAR(50),
  trial_start_date DATE NOT NULL,
  trial_end_date DATE NOT NULL,
  status ENUM('trial', 'paid', 'cancelled', 'expired') DEFAULT 'trial',
  max_users_during_trial INT DEFAULT 1,
  current_plan VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ユーザー使用状況ログ
CREATE TABLE usage_logs (
  id INT PRIMARY KEY AUTO_INCREMENT,
  contract_id INT,
  date DATE NOT NULL,
  active_users_count INT NOT NULL,
  peak_concurrent_users INT NOT NULL,
  FOREIGN KEY (contract_id) REFERENCES contracts(id)
);

-- メール送信履歴
CREATE TABLE email_logs (
  id INT PRIMARY KEY AUTO_INCREMENT,
  contract_id INT,
  email_type ENUM('welcome', 'trial_reminder', 'billing_notice', 'cancellation') NOT NULL,
  sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status ENUM('sent', 'failed', 'pending') DEFAULT 'pending',
  FOREIGN KEY (contract_id) REFERENCES contracts(id)
);
```

### 2. **自動メール送信システム**

#### GAS トリガー設定
```javascript
// 日次実行トリガー（毎日午前9時）
function createDailyTrigger() {
  ScriptApp.newTrigger('checkTrialStatus')
    .timeBased()
    .everyDays(1)
    .atHour(9)
    .create();
}

// トライアル状況チェック関数
function checkTrialStatus() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('contracts');
  const data = sheet.getDataRange().getValues();
  
  const today = new Date();
  
  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    const contractId = row[0];
    const email = row[4];
    const trialStartDate = new Date(row[7]);
    const trialEndDate = new Date(row[8]);
    const status = row[9];
    
    if (status !== 'trial') continue;
    
    const daysRemaining = Math.ceil((trialEndDate - today) / (1000 * 60 * 60 * 24));
    
    // 12日目（2日前）に有料移行お知らせメール送信
    if (daysRemaining === 2) {
      sendTrialReminderEmail(contractId, email, row);
    }
    
    // 15日目（1日後）に請求書送信
    if (daysRemaining === -1) {
      processTrialExpiry(contractId, row);
    }
  }
}
```

#### メールテンプレート設計

**1. トライアル2日前通知メール**
```javascript
function sendTrialReminderEmail(contractId, email, contractData) {
  const subject = '【TeamBase】無料トライアル期間終了のお知らせ（2日前）';
  
  const htmlBody = `
    <div style="max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif;">
      <h2>無料トライアル期間終了のお知らせ</h2>
      
      <p>${contractData[3]} 様</p>
      
      <p>TeamBaseの無料トライアルをご利用いただき、ありがとうございます。</p>
      
      <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <h3>🔔 重要なお知らせ</h3>
        <p>あと<strong>2日</strong>で無料トライアル期間が終了します。</p>
        <ul>
          <li>トライアル期間中の最大利用ユーザー数: <strong>${getMaxUsers(contractId)}名</strong></li>
          <li>適用予定プラン: <strong>${calculatePlan(getMaxUsers(contractId))}</strong></li>
          <li>月額料金: <strong>¥${calculatePrice(getMaxUsers(contractId))}</strong></li>
        </ul>
      </div>
      
      <h3>📅 今後のスケジュール</h3>
      <ul>
        <li><strong>${new Date(Date.now() + 2*24*60*60*1000).toLocaleDateString()}</strong>: トライアル期間終了</li>
        <li><strong>${new Date(Date.now() + 3*24*60*60*1000).toLocaleDateString()}</strong>: 請求書発行・送付</li>
      </ul>
      
      <div style="text-align: center; margin: 30px 0;">
        <a href="https://your-domain.com/cancel?token=${generateCancelToken(contractId)}" 
           style="background: #dc3545; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin-right: 10px;">
          解約する
        </a>
        <a href="https://your-domain.com/continue?token=${generateContinueToken(contractId)}" 
           style="background: #4A6FFF; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px;">
          継続利用する
        </a>
      </div>
      
      <p style="font-size: 14px; color: #666;">
        このメールへの返信でも解約のお申し出を承ります。<br>
        ご不明な点がございましたら、お気軽にお問い合わせください。
      </p>
    </div>
  `;
  
  MailApp.sendEmail({
    to: email,
    subject: subject,
    htmlBody: htmlBody
  });
}
```

### 3. **課金・請求処理**

#### 請求書生成システム
```javascript
function processTrialExpiry(contractId, contractData) {
  const maxUsers = getMaxUsers(contractId);
  const plan = calculatePlan(maxUsers);
  const amount = calculatePrice(maxUsers);
  
  // ステータスを有料プランに更新
  updateContractStatus(contractId, 'paid', plan);
  
  // 請求書生成
  const invoiceData = {
    contractId: contractId,
    companyName: contractData[1],
    contactName: contractData[3],
    email: contractData[4],
    maxUsers: maxUsers,
    plan: plan,
    amount: amount,
    issueDate: new Date(),
    dueDate: new Date(Date.now() + 30*24*60*60*1000) // 30日後
  };
  
  generateInvoice(invoiceData);
  sendInvoiceEmail(invoiceData);
}

function calculatePlan(userCount) {
  return '基本料金プラン';
}

function calculatePrice(userCount) {
  return userCount * 10000; // 1ユーザーあたり10,000円
}
```

### 4. **解約処理システム**

#### 解約フォーム
```html
<!-- cancel.html -->
<form id="cancelForm">
  <h2>TeamBase 解約お手続き</h2>
  
  <div class="form-group">
    <label>解約理由（任意）</label>
    <select name="reason">
      <option value="">選択してください</option>
      <option value="price">料金が高い</option>
      <option value="features">機能が不足</option>
      <option value="usability">使いにくい</option>
      <option value="other">その他</option>
    </select>
  </div>
  
  <div class="form-group">
    <label>ご意見・ご要望（任意）</label>
    <textarea name="feedback" rows="4"></textarea>
  </div>
  
  <button type="submit" class="btn-danger">解約する</button>
  <a href="/dashboard" class="btn-secondary">継続利用する</a>
</form>
```

### 5. **ダッシュボード機能**

#### 管理者画面
- トライアル中の企業一覧
- 期限切れ間近の企業アラート
- 月次売上レポート
- 解約理由分析

#### ユーザー画面
- トライアル残日数表示
- 現在の利用ユーザー数
- 予定料金シミュレーション

## 🚀 実装ステップ

### Phase 1: 基盤構築（1-2週間）
1. データベース設計・構築
2. GAS基本機能実装
3. メール送信機能

### Phase 2: 自動化（2-3週間）
1. トリガー設定
2. 日次バッチ処理
3. 課金ロジック実装

### Phase 3: UI構築（2-3週間）
1. 解約フォーム作成
2. 管理者ダッシュボード
3. ユーザーダッシュボード

### Phase 4: テスト・運用（1週間）
1. 統合テスト
2. 本番環境構築
3. 運用開始

## 📊 KPI・監視項目

- トライアル→有料転換率
- 解約率（トライアル中、有料後）
- 平均利用ユーザー数
- 月次売上高
- メール開封率・クリック率

## 🔒 セキュリティ考慮事項

- 解約トークンの暗号化
- 個人情報の適切な管理
- 支払情報の セキュア処理
- アクセスログの記録

## 💡 運用上の注意点

- メール配信の失敗処理
- 祝日・土日の請求処理
- 大量解約時の対応フロー
- カスタマーサポート体制 