# SL.AI Team Base

シンプルで直感的なタスク管理ツール。チームの生産性を最大化し、組織の目標達成をサポートします。

## 概要

TeamBaseは、以下の課題を解決する組織マネジメントツールです：

- 各部署のタスクと目標の可視化
- KPIと業務のつながりの明確化
- マネジメント層の管理負担の軽減

## 主な機能

### 1. 組織活動の可視化
- 各部署のKPIと所属メンバーのTodoを一括管理
- リアルタイムな進捗状況の共有
- 直感的なダッシュボード

### 2. KPI管理
- 目標設定と期限管理
- 進捗状況のトラッキング
- レポート機能

### 3. Todo管理
- タスクの割り振りと管理
- チームメンバー間の連携
- モバイル対応

## プロジェクト構成

```
TeamBase/
├── 🏠 メインページ
│   ├── index.html              # トップページ
│   ├── signup.html             # 申し込みフォーム
│   ├── confirm.html            # プラン選択・確認ページ
│   └── complete.html           # 申し込み完了ページ
│
├── 🎓 オンボーディングフロー
│   ├── step1-todo.html         # Step1: Todo App登録
│   ├── step2-teambase.html     # Step2: TeamBase登録
│   └── teambase-academy.html   # Step3: Academy学習
│
├── 🔧 解約システム
│   ├── cancellation-form.html           # 解約申請フォーム
│   ├── cancellation-gas-script.txt      # 統合GASスクリプト
│   └── cancellation-system-setup-guide.md # 設定ガイド
│
├── 📄 サポートページ
│   ├── terms.html              # 利用規約
│   ├── privacy.html            # プライバシーポリシー
│   ├── vision.html             # ビジョンページ
│   └── payment.html            # 決済ページ
│
├── 📚 ドキュメント
│   ├── README.md               # プロジェクト説明
│   └── pricing-plan.md         # 料金プラン
│
└── 🛠️ 開発環境
    ├── package.json            # Node.js依存関係
    ├── server.js               # 開発サーバー
    └── images/                 # 画像ファイル
```

## 新機能: 3段階オンボーディングフロー

### Step 1: Todo App登録
- Todo Appアカウント作成ガイド
- 完了チェックボックス機能
- 進捗保存機能

### Step 2: TeamBase登録
- TeamBaseアカウント作成
- 組織情報入力サポート
- 前ステップ依存チェック

### Step 3: Academy学習
- 10本の学習動画
- ブックマーク推奨機能
- 組織マネジメント完全マスター

## 新機能: 解約管理システム

### 解約申請フォーム
- 詳細な解約理由収集
- 今後の連絡設定
- 美しいUIデザイン

### 統合管理システム
- 申し込み〜解約まで一元管理
- 自動メール通知
- スプレッドシート連携

## ステータス管理システム（日本語対応）

### トライアル進捗の流れ
```
1. 申し込み → 2. トライアル開始 → 3. 分岐点（14日後）
                                      ├── 解約
                                      └── 有料継続
```

### ステータス一覧
| ステータス | 説明 | 期間/条件 |
|-----------|------|----------|
| `トライアル申込完了` | 申し込み完了、トライアル開始 | 申し込み直後 |
| `トライアル利用中` | 14日間無料トライアル期間 | 申し込み後1-11日 |
| `トライアル期限間近` | 期限が近づいている状態 | 残り3日以下 |
| `解約済み` | トライアル期間中に解約申請 | 解約フォーム送信後 |
| `有料契約移行` | トライアル終了後の継続利用 | 14日後、解約なしの場合 |
| `期限切れ` | トライアル期間終了（未決定） | 14日後、継続手続き未完了 |

## 料金プラン

1. **14日間無料トライアル**
   - 完全無料
   - 全機能利用可能
   - チーム全体での利用
   - いつでも解約可能

2. **基本料金**
   - ¥10,000/ユーザー・月（税込）
   - 全機能利用可能
   - 無制限のタスク管理
   - チームコラボレーション機能
   - レポート・分析機能
   - メールサポート

## 開発環境

- HTML5
- CSS3
- JavaScript
- Google Apps Script (GAS)
- Node.js（開発サーバー）

## ローカル開発環境の構築

1. リポジトリのクローン
```bash
git clone https://github.com/addness-info-osaka/TeamBase.git
cd TeamBase
```

2. 開発サーバーの起動
```bash
npm install
npm start
# または
python3 -m http.server 3000
```

3. ブラウザでアクセス
```
http://localhost:3000
```

## デプロイ情報

### GitHub Pages
- **URL**: https://addness-info-osaka.github.io/TeamBase/
- **Step1**: https://addness-info-osaka.github.io/TeamBase/step1-todo.html
- **Academy**: https://addness-info-osaka.github.io/TeamBase/teambase-academy.html

### Google Apps Script
- **統合WebアプリURL**: 申し込み・解約処理統合スクリプト
- **機能**: スプレッドシート管理、メール通知、データ処理

## システム構成

```
[申し込みフォーム] → [GAS] → [スプレッドシート] → [メール通知]
        ↓              ↓            ↓            ↓
[Step1-2-3フロー] → [学習完了] → [利用開始] → [継続/解約]
        ↓                                      ↓
[Academy学習]                            [解約フォーム]
```

## お問い合わせ

詳細については各ページのお問い合わせフォームをご利用ください。

## ライセンス

© 2025 SL.AI Team Base. All Rights Reserved.