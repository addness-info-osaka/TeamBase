# TeamBase シンプルトライアル管理システム概要

## 🎯 **理想の流れ（実現済み）**

### 1️⃣ **申し込みフロー**
1. `signup.html` - 申し込みフォーム入力
2. `confirm.html` - 確認ページ（利用規約同意）
3. `gas-script-updated.txt` - GASでスプレッドシート保存 + メール送信
4. `onboarding.html` - トライアル開始

### 2️⃣ **トライアル管理フロー**
5. `simple-trial-management.txt` - 毎日自動チェック（午前9時）
6. **12日目**：自動通知メール送信（解約案内含む）
7. **解約の場合**：`cancel-form.html` → `cancellation-gas-script.txt`
8. **継続の場合**：自動的に有料プラン移行

## 📁 **ファイル構成**

### **フロントエンド**
- ✅ `index.html` - ランディングページ
- ✅ `signup.html` - 申し込みフォーム
- ✅ `confirm.html` - 確認ページ
- ✅ `cancel-form.html` - 解約申し込みフォーム
- ✅ `onboarding.html` - オンボーディング

### **GASスクリプト**
- ✅ `gas-script-updated.txt` - 申し込み処理用
- ✅ `simple-trial-management.txt` - トライアル管理用  
- ✅ `cancellation-gas-script.txt` - 解約処理用

### **削除したファイル**
- ❌ `trial-management-gas-script.txt` - 複雑すぎるため削除
- ❌ `trial-reminder-email-template.html` - GASに統合済みで削除

## 🔧 **必要な設定**

### **GAS設定手順**
1. **申し込み処理GAS**
   - `gas-script-updated.txt` を新規GASプロジェクトに設定
   - Webアプリとして公開
   - URLを `confirm.html` に設定

2. **トライアル管理GAS**
   - `simple-trial-management.txt` を同じスプレッドシートに設定
   - `setupDailyTrigger()` を実行してトリガー設定

3. **解約処理GAS**
   - `cancellation-gas-script.txt` を新規GASプロジェクトに設定
   - Webアプリとして公開
   - URLを `cancel-form.html` に設定

### **スプレッドシート列構成**
- A列: タイムスタンプ
- B列: 担当者名
- C列: メールアドレス
- D列: 電話番号
- E列: 部署名
- F列: 従業員数
- G列: 導入目的
- H列: メール送信状態
- I列: 会社名
- J列: ステータス (`trial` → `reminder_sent` → `cancelled`/`paid`)
- K列: 解約理由
- L列: 詳細理由
- M列: 解約日時

## 📧 **メール送信パターン**

### **申し込み時**
- 管理者：新規申し込み通知
- 申し込み者：確認メール（オンボーディングリンク付き）

### **12日目通知**
- 申し込み者：有料プラン移行通知（解約フォームリンク付き）
- 管理者：通知送信完了報告

### **解約時**
- 管理者：解約申し込み通知
- 申し込み者：解約完了確認メール

## 🎯 **ステータス管理**

| ステータス | 説明 | 次のアクション |
|------------|------|----------------|
| `trial` / `pending_approval` | トライアル中 | 12日目で通知 |
| `reminder_sent` | 通知送信済み | 解約待ち |
| `cancelled` | 解約済み | 処理完了 |
| `paid` | 有料プラン移行 | 請求開始 |

## ✅ **完了事項**
- ✅ シンプルで実用的な構成に変更
- ✅ 複雑な価格計算機能を削除
- ✅ 解約フォームと処理機能を追加
- ✅ 不要ファイルを削除
- ✅ 明確なファイル構成とフロー

## 🚀 **次のステップ**
1. GASスクリプトをスプレッドシートに設定
2. WebアプリURLをHTMLファイルに反映
3. 実際のドメインでテスト実行 