# データフロー

システム内のデータの流れを可視化し、説明します。

## 概要

このドキュメントでは、フロントエンドからバックエンド、データベースまでのデータの流れを明確にします。

---

## 全体データフロー

```mermaid
sequenceDiagram
    participant User as ユーザー
    participant FE as Frontend
    participant API as API Server
    participant Cache as Redis Cache
    participant DB as Database
    participant Storage as Object Storage

    User->>FE: アクション
    FE->>API: APIリクエスト (JWT)
    
    API->>API: 認証・認可チェック
    
    alt キャッシュヒット
        API->>Cache: キャッシュ確認
        Cache-->>API: キャッシュデータ
    else キャッシュミス
        API->>DB: データ取得
        DB-->>API: データ
        API->>Cache: キャッシュ更新
    end
    
    API-->>FE: レスポンス
    FE-->>User: 結果表示
```

---

## ユースケース別データフロー

### 1. ユーザー登録フロー

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant DB
    participant Email

    User->>Frontend: 登録フォーム送信
    Frontend->>API: POST /api/v1/auth/register
    
    API->>API: バリデーション
    API->>DB: メール重複チェック
    
    alt メール重複
        DB-->>API: エラー
        API-->>Frontend: 409 Conflict
        Frontend-->>User: エラー表示
    else メール未使用
        API->>DB: ユーザー作成
        API->>DB: プロフィール作成
        API->>API: JWT生成
        API->>Email: 認証メール送信
        API-->>Frontend: 201 Created + JWT
        Frontend->>Frontend: トークン保存
        Frontend-->>User: 登録完了
    end
```

### 2. ログインフロー

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant DB
    participant Cache

    User->>Frontend: ログインフォーム送信
    Frontend->>API: POST /api/v1/auth/login
    
    API->>DB: ユーザー情報取得
    API->>API: パスワード検証
    
    alt 認証成功
        API->>API: JWT生成
        API->>Cache: セッション情報保存
        API->>DB: last_login更新
        API-->>Frontend: 200 OK + JWT
        Frontend->>Frontend: トークン保存
        Frontend-->>User: ログイン成功
    else 認証失敗
        API-->>Frontend: 401 Unauthorized
        Frontend-->>User: エラー表示
    end
```

### 3. 投稿作成フロー

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant DB
    participant Cache
    participant Storage

    User->>Frontend: 投稿作成
    Frontend->>API: POST /api/v1/posts (JWT)
    
    API->>API: JWT検証
    API->>DB: トランザクション開始
    
    alt 画像あり
        API->>Storage: 画像アップロード
        Storage-->>API: 画像URL
    end
    
    API->>DB: 投稿作成
    API->>DB: タグ関連付け
    API->>DB: コミット
    
    API->>Cache: キャッシュ無効化
    
    API-->>Frontend: 201 Created
    Frontend-->>User: 投稿完了
```

### 4. 投稿一覧取得フロー（キャッシュ活用）

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant Cache
    participant DB

    User->>Frontend: 投稿一覧表示
    Frontend->>API: GET /api/v1/posts
    
    API->>Cache: キャッシュキー生成<br/>(page, filters, sort)
    API->>Cache: キャッシュ確認
    
    alt キャッシュヒット
        Cache-->>API: キャッシュデータ
        API-->>Frontend: 200 OK (from cache)
    else キャッシュミス
        API->>DB: クエリ実行
        DB-->>API: データ
        API->>Cache: キャッシュ保存 (TTL: 5分)
        API-->>Frontend: 200 OK
    end
    
    Frontend-->>User: 一覧表示
```

### 5. コメント投稿フロー（リアルタイム通知）

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant DB
    participant Cache
    participant WebSocket

    User->>Frontend: コメント投稿
    Frontend->>API: POST /api/v1/posts/:id/comments
    
    API->>API: JWT検証
    API->>DB: 投稿存在確認
    API->>DB: コメント作成
    
    API->>Cache: 投稿キャッシュ無効化
    
    API->>WebSocket: コメント通知配信
    WebSocket-->>Frontend: リアルタイム更新
    
    API-->>Frontend: 201 Created
    Frontend-->>User: コメント表示
```

---

## データ永続化フロー

### 書き込み処理

```
[Frontend] 
    ↓ HTTP POST/PUT
[API Server]
    ↓ バリデーション
[Business Logic]
    ↓ データ変換
[Repository Layer]
    ↓ SQL生成
[Database (PostgreSQL)]
    ↓ トリガー実行
[Audit Log / Cache Invalidation]
```

### 読み取り処理

```
[Frontend]
    ↓ HTTP GET
[API Server]
    ↓ 認証・認可
[Cache Layer (Redis)]
    ├─ Cache Hit → [Response]
    └─ Cache Miss
        ↓
    [Database (PostgreSQL)]
        ↓ Read Replica
    [Response + Cache Update]
```

---

## エラーハンドリングフロー

```mermaid
flowchart TD
    A[リクエスト受信] --> B{認証チェック}
    B -->|失敗| C[401 Unauthorized]
    B -->|成功| D{認可チェック}
    D -->|失敗| E[403 Forbidden]
    D -->|成功| F{バリデーション}
    F -->|失敗| G[400 Bad Request]
    F -->|成功| H{ビジネスロジック}
    H -->|失敗| I[422 Unprocessable]
    H -->|成功| J{データベース処理}
    J -->|失敗| K[500 Internal Error]
    J -->|成功| L[200/201 Success]
    
    K --> M[エラーログ記録]
    M --> N[アラート通知]
```

---

## データ同期フロー

### フロントエンド状態管理

```
[Server State]
    ↓ API Call
[React Query / Redux]
    ↓ Cache
[Local State]
    ↓ UI Update
[User Interface]

[Optimistic Update]
    ↓ 即座にUI更新
[Background Sync]
    ↓ APIコール
[Success] → [確定]
[Failure] → [ロールバック]
```

---

## バッチ処理フロー

### 定期実行ジョブ

```mermaid
graph LR
    A[Scheduler<br/>Cron] --> B[Job Queue<br/>Celery/Bull]
    B --> C[Worker 1]
    B --> D[Worker 2]
    B --> E[Worker N]
    
    C --> F[Database]
    D --> F
    E --> F
    
    F --> G[Result Queue]
    G --> H[Notification<br/>Service]
```

**例: 日次集計ジョブ**

1. 毎日深夜2時にスケジューラーが起動
2. ジョブキューにタスクを追加
3. ワーカーが並列処理
4. 集計結果をデータベースに保存
5. 完了通知を送信

---

## ファイルアップロードフロー

### 直接アップロード（S3 Presigned URL）

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant S3

    User->>Frontend: ファイル選択
    Frontend->>API: POST /api/v1/upload/presigned-url
    API->>API: 権限チェック
    API->>S3: Presigned URL生成
    S3-->>API: Presigned URL
    API-->>Frontend: Presigned URL
    
    Frontend->>S3: PUT (直接アップロード)
    S3-->>Frontend: 200 OK
    
    Frontend->>API: POST /api/v1/posts (画像URL含む)
    API->>API: URL検証
    API-->>Frontend: 201 Created
```

---

## WebSocket通信フロー

### リアルタイム通知

```mermaid
sequenceDiagram
    participant User1
    participant Frontend1
    participant WSServer
    participant API
    participant Frontend2
    participant User2

    Frontend1->>WSServer: WebSocket接続
    Frontend2->>WSServer: WebSocket接続
    
    User1->>Frontend1: コメント投稿
    Frontend1->>API: POST /api/v1/comments
    API->>API: コメント保存
    API->>WSServer: イベント発行
    
    WSServer->>Frontend1: 更新通知
    WSServer->>Frontend2: 更新通知
    
    Frontend1-->>User1: リアルタイム表示
    Frontend2-->>User2: リアルタイム表示
```

---

## データ変換フロー

### レイヤー別データ形式

```
[Frontend - TypeScript Interface]
interface Post {
  postId: string;
  title: string;
  createdAt: Date;
}

[API - JSON]
{
  "post_id": "uuid",
  "title": "string",
  "created_at": "2024-01-01T00:00:00Z"
}

[Backend - Python Model]
class Post:
    post_id: UUID
    title: str
    created_at: datetime

[Database - SQL]
posts (
  post_id UUID,
  title VARCHAR(255),
  created_at TIMESTAMP
)
```

### 変換タイミング

1. **Frontend → API**: camelCase → snake_case
2. **API → Backend**: JSON → Python Object
3. **Backend → Database**: ORM Model → SQL
4. **Database → Backend**: SQL Result → ORM Model
5. **Backend → API**: Python Object → JSON
6. **API → Frontend**: snake_case → camelCase

---

## セキュリティフロー

### 認証・認可フロー

```
[Request] 
    ↓
[Rate Limiter] (過剰なリクエストをブロック)
    ↓
[JWT Verification] (トークンの有効性確認)
    ↓
[User Context] (ユーザー情報をコンテキストに格納)
    ↓
[Authorization] (リソースへのアクセス権限確認)
    ↓
[Resource Access]
```

### データ暗号化フロー

```
[User Input]
    ↓ HTTPS (TLS 1.3)
[API Server]
    ↓ 機密データ暗号化
[Database]
    ↓ 暗号化ストレージ (AES-256)
[Disk]
```

---

## モニタリングとログ

### ログ収集フロー

```mermaid
graph LR
    A[Application] --> B[Fluentd/Logstash]
    C[Database] --> B
    D[Web Server] --> B
    
    B --> E[Elasticsearch]
    E --> F[Kibana<br/>可視化]
    E --> G[Alerting<br/>アラート]
```

### メトリクス収集フロー

```mermaid
graph LR
    A[Application] --> B[Prometheus]
    C[Database] --> B
    D[Infrastructure] --> B
    
    B --> E[Grafana<br/>ダッシュボード]
    B --> F[Alertmanager<br/>アラート]
```

---

## パフォーマンス最適化

### N+1問題の解決

**Before (N+1クエリ)**:
```
1. 投稿一覧取得 (1クエリ)
2. 各投稿の著者情報取得 (Nクエリ)
→ 合計 N+1 クエリ
```

**After (Eager Loading)**:
```
1. 投稿一覧 + 著者情報を JOIN で取得 (1クエリ)
→ 合計 1 クエリ
```

### クエリ最適化フロー

```
[Original Query]
    ↓ Analyze
[EXPLAIN]
    ↓ Identify Bottleneck
[Index Creation / Query Rewrite]
    ↓ Test
[Performance Improvement]
```

---

## データフロー更新履歴

| 日付 | 変更内容 | 理由 | 担当者 |
|-----|---------|------|--------|
| [YYYY-MM-DD] | [変更内容] | [理由] | [担当者] |
