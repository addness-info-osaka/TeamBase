# TeamBase 解約フォームシステム 設定ガイド

## 📋 概要

TeamBase の解約申請を管理するシステムです。既存の申し込み管理スプレッドシートに解約情報を統合して記録し、管理者と申請者に自動でメール通知を送信します。

## 🗂️ ファイル構成

```
解約システム/
├── cancellation-form.html           # 解約申請フォーム
├── cancellation-gas-script.txt      # GAS統合スクリプト
└── cancellation-system-setup-guide.md # 設定ガイド（このファイル）
```

## 🚀 セットアップ手順

### 1. スプレッドシートの準備

#### 1.1 既存スプレッドシートの確認
- 既存の申し込み管理スプレッドシートを開く
- 現在の列構成を確認

#### 1.2 新しい列の追加
既存の列（A〜K列）の後に、以下の列を追加してください：

| 列 | 項目名 | 説明 |
|---|--------|------|
| L | 解約理由 | 選択された解約理由 |
| M | 解約詳細理由 | ユーザーが入力した詳細な理由 |
| N | 今後の連絡許可 | 製品改善情報の受信許可 |
| O | マーケティング連絡許可 | 新サービス情報の受信許可 |
| P | 希望連絡日時 | 担当者からの連絡希望日時 |
| Q | 追加メッセージ | 担当者への追加メッセージ |
| R | 解約ステータス | 解約処理の現在状況 |

#### 1.3 自動ヘッダー設定（推奨）
GASスクリプトの `setupSpreadsheetHeaders()` 関数を実行すると、自動でヘッダー行を設定できます。

### 2. Google Apps Script (GAS) の設定

#### 2.1 スクリプトの追加
1. スプレッドシートを開く
2. 「拡張機能」→「Apps Script」をクリック
3. `cancellation-gas-script.txt` の内容をコピー＆ペースト
4. 既存の `doPost` 関数を置き換える

#### 2.2 設定値の変更
スクリプト上部の設定値を環境に合わせて変更：

```javascript
// 管理者のメールアドレス
const ADMIN_EMAIL = 'info.osaka@addness.co.jp'; // ← 実際の管理者メールに変更

// 会社からの送信者名
const COMPANY_NAME = 'SL.AI Team Base';
const COMPANY_EMAIL = 'noreply@sl-ai.com'; // ← 必要に応じて変更
```

#### 2.3 Webアプリとして公開
1. 「デプロイ」→「新しいデプロイ」をクリック
2. 「種類」で「ウェブアプリ」を選択
3. 以下の設定で公開：
   - 実行ユーザー: 自分
   - アクセス権限: 全員
4. 生成されたWebアプリURLをコピー

### 3. 解約フォームの設定

#### 3.1 GAS WebアプリURLの設定
`cancellation-form.html` の以下の部分を変更：

```javascript
// 実際のGAS WebアプリURLに変更
const GAS_URL = 'YOUR_GAS_WEB_APP_URL'; // ← ここに生成されたURLを入力
```

#### 3.2 フォームのアップロード・リンク設定
- GitHub Pagesに `cancellation-form.html` をアップロード
- **解約フォームURL**: `https://addness-info-osaka.github.io/TeamBase/cancellation-form.html`
- **Step1オンボーディングURL**: `https://addness-info-osaka.github.io/TeamBase/step1-todo.html`
- **Academy学習ページURL**: `https://addness-info-osaka.github.io/TeamBase/teambase-academy.html`
- **新しいGAS WebアプリURL**: `https://script.google.com/macros/s/AKfycby8c-COR2eZUdjSpxautLiqAu4Qdewf5vEZolikW6WlWZi9yVWTD-nB3jLLNhteb-CdjA/exec`

## 📊 データ管理

### スプレッドシートでの管理方法

#### 申し込み情報の確認
- **ステータス列（J列）**で顧客の状態を確認
  - `申し込み中` : 新規申し込み
  - `解約申請中` : 解約申請済み
  - `解約完了` : 解約処理完了

#### 解約処理の流れ
1. **解約申請受付** → 解約ステータス（R列）に記録
2. **担当者による確認連絡**
3. **解約処理実行** → ステータスを「解約完了」に更新
4. **完了通知送信**

### 重要な処理チェックリスト

解約処理実行時は以下を確認：
- [ ] アカウントの無効化
- [ ] 請求処理の停止  
- [ ] データのバックアップ（必要に応じて）
- [ ] データの削除
- [ ] 解約完了通知の送信

## 📧 メール通知システム

### 管理者への通知メール
解約申請があると自動で送信されます：
- 申請者の基本情報
- 解約理由と詳細
- 既存顧客か新規申請かの判別
- 処理チェックリスト

### 申請者への確認メール
申請者に自動で送信されます：
- 申請内容の確認
- 今後の流れの説明
- 注意事項
- 連絡先情報

## 🔧 カスタマイズ

### 解約理由の追加・変更
`cancellation-form.html` と GAS スクリプトの両方で修正が必要です：

#### フォーム側（HTML）
```html
<label class="reason-option">
  <input type="radio" name="cancellationReason" value="新しい理由コード" required>
  <span>🆕 新しい解約理由</span>
</label>
```

#### GAS側（JavaScript）
```javascript
function getCancellationReasonText(reasonCode) {
  const reasonMap = {
    // 既存の理由...
    '新しい理由コード': '🆕 新しい解約理由'
  };
  return reasonMap[reasonCode] || reasonCode;
}
```

### メールテンプレートの変更
GAS スクリプトの以下の関数でメール内容を変更できます：
- `sendCancellationNotificationToAdmin()` : 管理者向けメール
- `sendCancellationConfirmationEmail()` : 申請者向けメール

## 🔍 トラブルシューティング

### よくある問題と解決方法

#### 1. フォーム送信でエラーが発生する
- GAS WebアプリURLが正しく設定されているか確認
- GASスクリプトが正しく公開されているか確認
- ブラウザの開発者ツールでエラーログを確認

#### 2. メールが送信されない
- 管理者メールアドレスが正しく設定されているか確認
- GASの実行権限を確認
- Gmail の送信制限に達していないか確認

#### 3. スプレッドシートに記録されない
- スプレッドシートのアクセス権限を確認
- GASスクリプトがスプレッドシートにバインドされているか確認
- 列番号の定義が正しいか確認

#### 4. 既存顧客が見つからない
- 会社名とメールアドレスの完全一致を確認
- スプレッドシートの会社名列（I列）にデータがあるか確認

## 📝 ログとデバッグ

### デバッグモードの有効化
GAS スクリプトの上部で設定：
```javascript
const DEBUG = true; // デバッグログを出力
```

### ログの確認方法
1. GAS エディタを開く
2. 「実行ログ」タブでログを確認
3. エラーの詳細情報を確認

## 🔒 セキュリティ考慮事項

- GAS WebアプリのURLは外部に漏洩しないよう注意
- 管理者メールアドレスは適切なアクセス権限を持つアカウントを使用
- 個人情報の取り扱いに関する社内規定に従う
- 定期的にスプレッドシートのアクセス権限を確認

## 📞 サポート

システムに関する質問やトラブルがある場合は、開発担当者までお問い合わせください。

---

**最終更新日**: 2025年1月
**作成者**: SL.AI Team Base 開発チーム 