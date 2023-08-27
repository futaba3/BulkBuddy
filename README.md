# BulkBuddy要件定義書(最終更新 8/25 2:10)

# Github開発方針

## 開発ルール

開発を行う際は下記のブランチルールに従う

また、常に最新のdevelopeブランチの状態になるようmerge処理を行う

## ブランチ

- main: 現在デプロイされているプロダクト
- develope: 開発中バージョンの中心
- develope/[Github名]/[開発の概要][IssueID]: 実用ブランチ例

例: `develope/Kento210/fix_id#1`

### Issueについて

作業する内容についてIssueを作成して作業するものとする。

### PRについて

各開発が終了した際はdevelopeブランチへPRを出すものとする。

また、PRを出した場合は各個人が自己レビューを行う。

PR申請者以外がレビューを行い問題ないと判断された場合はMerge処理を行う

### デブロイについて

Mainブランチが外部に公開する最新プロダクトとして更新された際にデブロイ作業を行うものとする.

# 基本情報

- 設計方針：基本機能（無料機能から作っていく）
- ログイン必須（sns無料は）
- team1_Userテーブル（id、名前、パスワード、身長、体重、年齢、消費カロリー、目標体重、目標期日）
- team1_Snsテーブル（id、名前、タイムスタンプ、内容、返信、いいね（ソートキー）、カテゴリー）

→ category：食事内容、トレーニング内容

- 強制有料プラン（7days）
- フロント、バック担当は3日目と一緒

### API Gateway情報

URL: [https://52cypecucj.execute-api.ap-northeast-1.amazonaws.com](https://52cypecucj.execute-api.ap-northeast-1.amazonaws.com/)
名前: angels-bulkbuddy-api

### Figmaリンク

[https://www.figma.com/file/YmrmPtm4u0zza8keNnLgQz/BulkBuddy?type=design&node-id=0%3A1&mode=design&t=aclGlTrtZTLTXDxm-1](https://www.figma.com/file/YmrmPtm4u0zza8keNnLgQz/BulkBuddy?type=design&node-id=0%3A1&mode=design&t=aclGlTrtZTLTXDxm-1)

### 目標設定機能

- 目標カロリーの設定
- 初回ログイン時のアンケート機能
- gender `1 = 男 2 = 女 3 = その他`

→基本アンケート項目

1. あなたの目標は？（希望体重）
2. 名前は？
3. 生年月日は？
4. 身長は？
5. 体重は？
6. アカウントの設定（パスワード、〇〇でサインアップなど）
7. （ポリシー、利用規約、Cookieポリシー）

→プラン診断

1. あなたの目標体重は？（number > number の形状）
2. ペース（2023年、12月、1日達成する！など）
3. 増量へのアプローチ方法は？（食事中心、食事とバランスよく、運動中心 <目標摂取カロリーと目標消費カロリーの表示> ）
4. コース、手段の提示（基本コース、〇〇コースなど）
5. 結果の表示（〇〇コースで、〇〇までに、〇〇kg、一日の摂取カロリー、朝昼晩の摂取カロリー）

### 記録管理

- その日の体重や摂取カロリーを記録する。
- 記録した結果から目標体重までの重量や一日に必要な摂取カロリーを表示する。

### フロントについて

- 

Userテーブル（id（プライマリーキー）、名前、パスワード、身長、体重、年齢、消費カロリー、目標体重、目標期日）

### API仕様書

|  |  |  | リクエストパラメータ |  |  | レスポンス内容 |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| メゾット | エントリーポイント | 処理の内容 | 変数名 | 型 | 必須 | 変数名 | 型 |
| POST | /user/signup | ユーザの登録 | userId | string | ○ | userId | string |
|  |  |  | name | string | ○ | name | string |
|  |  |  | password | string | ○ |  |  |
|  |  |  | height | number | ○ | height | number |
|  |  |  | weight | number | ○ | weight | number |
|  |  |  | birth_year | number | ○ | birth_year | number |
|  |  |  | birth_month | number | ○ | birth_month | number |
|  |  |  | birth_day | number | ○ | birth_day | number |
|  |  |  |  |  |  | calorie | number |
|  |  |  | targetWeight | number |  | targetWeight | number |
|  |  | アドバンス | targetDate | number |  | targetData | number |
|  |  |  | gender | number | ○ |  |  |
|  |  |  |  |  |  | token | string |
| POST | /user/login | ユーザの認証 | userId | string | ○ | token | string |
|  |  |  | password | string | ○ |  |  |
| GET | /user | ユーザ情報の取得 | userId | string | ○ | userId | string |
|  |  |  |  |  |  | name | string |
|  |  |  |  |  |  | height | number |
|  |  |  |  |  |  | weight | number |
|  |  |  |  |  |  | age | number |
|  |  |  |  |  |  | calorie | number |
|  |  |  |  |  |  | targetWeight | number |
|  |  |  |  |  |  | targetDate | number |
|  |  |  |  |  |  | gender | number |
| PUT | /user | ユーザ情報の更新 | userId | string | ○ | userId | string |
|  |  |  | name | string |  | name | string |
|  |  |  | password | string |  |  |  |
|  |  |  | height | number |  | height | number |
|  |  |  | weight | number |  | weight | number |
|  |  |  | birth_year | number |  | birth_year | number |
|  |  |  | birth_month | number |  | birth_month | number |
|  |  |  | birth_day | number |  | birth_day | number |
|  |  |  | targetWeight | number |  | targetWeight | number |
|  |  |  | targetDate | number |  | targetData | number |
|  |  |  | gender | number |  | gender | number |
| DELETE | /user | ユーザの削除 | userId | string | ○ | success 200 |  |
| PUT | /user/record | カロリーの登録 | userId | string | ○ | userId | string |
|  |  |  | calorie | number | ○ | calorie | number |
|  |  |  | timestamp | number | （サーバ） | timestamp | number |

### コミュニティ機能

- sns写真なし、投稿、返信機能のみ

Snsテーブル（id（プライマリーキー）、名前、タイムスタンプ、内容、返信、いいね（ソートキー））

category=1は"食事"
category=2は"トレーニング"
category=3は"コラム"

### API仕様書

|  |  |  | リクエストパラメータ |  |  | レスポンス内容 |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| メゾット | エントリーポイント | 処理の内容 | 変数名 | 型 | 必須 | 変数名 | 型 |
| POST | /article | 投稿 | userId | string | ○ | userId | string |
|  |  |  | name | string | ○ | name | string |
|  |  |  | text | string | ○ | text | string |
|  |  |  | category | string |  | category | string |
|  |  |  |  |  |  | timestamp | number |
|  |  |  | reply | array (0) |  |  |  |
|  |  |  | likePost | number (0) |  |  |  |
| GET | /article/search | 検索 | userId | string |  | userId | string |
|  |  |  | category | string |  | name | string |
|  |  |  | likepost_search | number |  | text | string |
|  |  |  |  |  |  | category | string |
|  |  |  |  |  |  | reply | array (0) |
|  |  |  |  |  |  | likePost | number (0) |
| GET | /article | 表示 |  |  |  | articles | array |
| GET | /article/free | 制限表示 |  |  |  | articles | array |
| DELETE | /article | 削除 | userId | string | ○ | success 200 |  |
|  |  |  | timestamp | number | ○ |  |  |

### コラム機能 = SNS

- snsテーブルに保存
- 内容をtokenありとなしで表示方法を変える
- カテゴリーで検索、userId、いいねのソート

→デフォルト、timestampソート、`likepost = 1`のときいいねソート起動（デフォルトは0）

- 制限版：最新、3件まで

### Todoリストとリマインダー

- 時間余ったら

### APIの外部提供（アドバンス）

- 時間余ったら
