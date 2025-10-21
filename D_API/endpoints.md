# APIエンドポイント定義

APIの全エンドポイントとその仕様を定義します。

## 概要

このドキュメントでは、REST API（またはGraphQL）のエンドポイント、リクエスト・レスポンス形式、認証要件、エラーハンドリングを明確にします。

---

## API基本情報

| 項目 | 設定値 |
|-----|-------|
| ベースURL（開発） | `http://localhost:8000/api` |
| ベースURL（本番） | `https://api.example.com/api` |
| APIバージョン | v1 |
| プロトコル | HTTPS |
| データ形式 | JSON |
| 文字コード | UTF-8 |
| 認証方式 | Bearer Token (JWT) |

---

## 共通仕様

### リクエストヘッダー

```
Content-Type: application/json
Accept: application/json
Authorization: Bearer <token>  # 認証が必要なエンドポイントのみ
```

### レスポンス形式

#### 成功レスポンス

```json
{
  "success": true,
  "data": {
    // レスポンスデータ
  },
  "message": "Success message (optional)",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

#### エラーレスポンス

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": {} // オプション: 詳細情報
  },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### HTTPステータスコード

| コード | 説明 | 使用例 |
|-------|------|--------|
| 200 | OK | GET, PUT成功 |
| 201 | Created | POST成功（リソース作成） |
| 204 | No Content | DELETE成功 |
| 400 | Bad Request | バリデーションエラー |
| 401 | Unauthorized | 認証エラー |
| 403 | Forbidden | 権限エラー |
| 404 | Not Found | リソースが存在しない |
| 409 | Conflict | リソースの競合 |
| 422 | Unprocessable Entity | ビジネスロジックエラー |
| 429 | Too Many Requests | レート制限超過 |
| 500 | Internal Server Error | サーバーエラー |

### ページネーション

```
GET /api/v1/posts?page=1&per_page=20
```

レスポンス:
```json
{
  "success": true,
  "data": {
    "items": [...],
    "pagination": {
      "current_page": 1,
      "per_page": 20,
      "total_items": 100,
      "total_pages": 5,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

### フィルタリング・ソート

```
GET /api/v1/posts?status=published&sort=-created_at&tag=technology
```

- `status`: ステータスでフィルタ
- `sort`: ソート（`-`プレフィックスで降順）
- `tag`: タグでフィルタ

---

## エンドポイント一覧

### 認証 (Authentication)

| メソッド | エンドポイント | 説明 | 認証 |
|---------|--------------|------|------|
| POST | `/api/v1/auth/register` | ユーザー登録 | 不要 |
| POST | `/api/v1/auth/login` | ログイン | 不要 |
| POST | `/api/v1/auth/logout` | ログアウト | 必要 |
| POST | `/api/v1/auth/refresh` | トークンリフレッシュ | 必要 |
| POST | `/api/v1/auth/verify-email` | メール認証 | 不要 |
| POST | `/api/v1/auth/forgot-password` | パスワードリセット要求 | 不要 |
| POST | `/api/v1/auth/reset-password` | パスワードリセット | 不要 |

### ユーザー (Users)

| メソッド | エンドポイント | 説明 | 認証 |
|---------|--------------|------|------|
| GET | `/api/v1/users/me` | 現在のユーザー情報取得 | 必要 |
| PUT | `/api/v1/users/me` | 現在のユーザー情報更新 | 必要 |
| GET | `/api/v1/users/:id` | 特定ユーザー情報取得 | 不要 |
| GET | `/api/v1/users` | ユーザー一覧取得 | 不要 |

### プロフィール (Profiles)

| メソッド | エンドポイント | 説明 | 認証 |
|---------|--------------|------|------|
| GET | `/api/v1/profiles/:user_id` | プロフィール取得 | 不要 |
| PUT | `/api/v1/profiles/me` | 自分のプロフィール更新 | 必要 |

### 投稿 (Posts)

| メソッド | エンドポイント | 説明 | 認証 |
|---------|--------------|------|------|
| GET | `/api/v1/posts` | 投稿一覧取得 | 不要 |
| GET | `/api/v1/posts/:id` | 特定投稿取得 | 不要 |
| POST | `/api/v1/posts` | 投稿作成 | 必要 |
| PUT | `/api/v1/posts/:id` | 投稿更新 | 必要 |
| DELETE | `/api/v1/posts/:id` | 投稿削除 | 必要 |
| POST | `/api/v1/posts/:id/publish` | 投稿公開 | 必要 |
| GET | `/api/v1/posts/:id/versions` | 投稿バージョン履歴 | 必要 |

### コメント (Comments)

| メソッド | エンドポイント | 説明 | 認証 |
|---------|--------------|------|------|
| GET | `/api/v1/posts/:post_id/comments` | コメント一覧取得 | 不要 |
| POST | `/api/v1/posts/:post_id/comments` | コメント作成 | 必要 |
| PUT | `/api/v1/comments/:id` | コメント更新 | 必要 |
| DELETE | `/api/v1/comments/:id` | コメント削除 | 必要 |

### タグ (Tags)

| メソッド | エンドポイント | 説明 | 認証 |
|---------|--------------|------|------|
| GET | `/api/v1/tags` | タグ一覧取得 | 不要 |
| GET | `/api/v1/tags/:slug` | 特定タグ取得 | 不要 |
| POST | `/api/v1/tags` | タグ作成 | 必要 |

---

## エンドポイント詳細

### POST /api/v1/auth/register

**説明**: 新規ユーザー登録

**認証**: 不要

**リクエスト**:
```json
{
  "email": "user@example.com",
  "password": "SecureP@ssw0rd",
  "display_name": "John Doe"
}
```

**バリデーション**:
- `email`: 必須、メール形式、最大255文字、ユニーク
- `password`: 必須、8文字以上、英大小文字・数字・記号を含む
- `display_name`: 必須、1〜100文字

**レスポンス (201)**:
```json
{
  "success": true,
  "data": {
    "user": {
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "user@example.com",
      "display_name": "John Doe",
      "is_verified": false,
      "created_at": "2024-01-01T12:00:00Z"
    },
    "token": {
      "access_token": "eyJhbGc...",
      "refresh_token": "eyJhbGc...",
      "expires_in": 3600
    }
  },
  "message": "Registration successful. Please check your email for verification."
}
```

**エラー (400)**:
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "email": ["Email already exists"],
      "password": ["Password must contain at least one uppercase letter"]
    }
  }
}
```

---

### POST /api/v1/auth/login

**説明**: ユーザーログイン

**認証**: 不要

**リクエスト**:
```json
{
  "email": "user@example.com",
  "password": "SecureP@ssw0rd"
}
```

**レスポンス (200)**:
```json
{
  "success": true,
  "data": {
    "user": {
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "user@example.com",
      "display_name": "John Doe",
      "is_verified": true
    },
    "token": {
      "access_token": "eyJhbGc...",
      "refresh_token": "eyJhbGc...",
      "expires_in": 3600
    }
  }
}
```

**エラー (401)**:
```json
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid email or password"
  }
}
```

---

### GET /api/v1/posts

**説明**: 公開投稿一覧取得

**認証**: 不要

**クエリパラメータ**:
- `page`: ページ番号（デフォルト: 1）
- `per_page`: 1ページあたりの件数（デフォルト: 20、最大: 100）
- `status`: ステータスフィルタ（published/draft/archived）
- `tag`: タグでフィルタ
- `author_id`: 著者IDでフィルタ
- `sort`: ソート順（-created_at/-updated_at/-view_count）
- `search`: 検索キーワード（タイトル・本文を全文検索）

**リクエスト例**:
```
GET /api/v1/posts?page=1&per_page=20&status=published&sort=-created_at&tag=technology
```

**レスポンス (200)**:
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "post_id": "660e8400-e29b-41d4-a716-446655440000",
        "title": "Introduction to API Design",
        "content": "API design is...",
        "status": "published",
        "author": {
          "user_id": "550e8400-e29b-41d4-a716-446655440000",
          "display_name": "John Doe",
          "avatar_url": "https://example.com/avatar.jpg"
        },
        "tags": ["technology", "api", "design"],
        "view_count": 1234,
        "comment_count": 15,
        "published_at": "2024-01-01T12:00:00Z",
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T11:00:00Z"
      }
    ],
    "pagination": {
      "current_page": 1,
      "per_page": 20,
      "total_items": 150,
      "total_pages": 8,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

---

### POST /api/v1/posts

**説明**: 新規投稿作成

**認証**: 必要

**リクエスト**:
```json
{
  "title": "My New Post",
  "content": "This is the content of my post...",
  "status": "draft",
  "tags": ["technology", "programming"]
}
```

**バリデーション**:
- `title`: 必須、1〜255文字
- `content`: 必須、1文字以上
- `status`: オプション、draft/published/archived（デフォルト: draft）
- `tags`: オプション、配列、各タグは50文字以内

**レスポンス (201)**:
```json
{
  "success": true,
  "data": {
    "post": {
      "post_id": "660e8400-e29b-41d4-a716-446655440000",
      "title": "My New Post",
      "content": "This is the content...",
      "status": "draft",
      "author": {
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "display_name": "John Doe"
      },
      "tags": ["technology", "programming"],
      "view_count": 0,
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  },
  "message": "Post created successfully"
}
```

---

### PUT /api/v1/posts/:id

**説明**: 投稿更新

**認証**: 必要（自分の投稿のみ）

**リクエスト**:
```json
{
  "title": "Updated Title",
  "content": "Updated content...",
  "tags": ["technology", "api", "update"]
}
```

**レスポンス (200)**:
```json
{
  "success": true,
  "data": {
    "post": {
      "post_id": "660e8400-e29b-41d4-a716-446655440000",
      "title": "Updated Title",
      "content": "Updated content...",
      "status": "draft",
      "tags": ["technology", "api", "update"],
      "updated_at": "2024-01-01T13:00:00Z"
    }
  },
  "message": "Post updated successfully"
}
```

**エラー (403)**:
```json
{
  "success": false,
  "error": {
    "code": "FORBIDDEN",
    "message": "You don't have permission to edit this post"
  }
}
```

---

### DELETE /api/v1/posts/:id

**説明**: 投稿削除

**認証**: 必要（自分の投稿のみ）

**レスポンス (204)**:
```
No Content
```

**エラー (404)**:
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Post not found"
  }
}
```

---

## エラーコード一覧

| エラーコード | HTTPステータス | 説明 |
|------------|--------------|------|
| VALIDATION_ERROR | 400 | 入力データのバリデーションエラー |
| INVALID_CREDENTIALS | 401 | 認証情報が無効 |
| UNAUTHORIZED | 401 | 認証トークンが無効または期限切れ |
| FORBIDDEN | 403 | アクセス権限がない |
| NOT_FOUND | 404 | リソースが見つからない |
| CONFLICT | 409 | リソースが既に存在する |
| RATE_LIMIT_EXCEEDED | 429 | レート制限を超過 |
| INTERNAL_ERROR | 500 | サーバー内部エラー |

---

## レート制限

| エンドポイント | 制限 | ウィンドウ |
|--------------|------|----------|
| 認証エンドポイント | 5回 | 15分 |
| 一般APIエンドポイント | 100回 | 15分 |
| 検索エンドポイント | 30回 | 1分 |

**レート制限超過時のレスポンスヘッダー**:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1640995200
Retry-After: 900
```

---

## CORS設定

**許可オリジン**:
- 開発: `http://localhost:3000`
- 本番: `https://example.com`

**許可メソッド**: GET, POST, PUT, DELETE, OPTIONS

**許可ヘッダー**: Content-Type, Authorization

---

## APIバージョニング

### URL バージョニング

現在のバージョン: v1

```
/api/v1/posts
/api/v2/posts  # 将来のバージョン
```

### 非推奨化ポリシー

1. 新バージョンリリース後、旧バージョンは6ヶ月サポート
2. 非推奨3ヶ月前に通知
3. レスポンスヘッダーに非推奨警告を含める

```
Deprecation: true
Sunset: Wed, 01 Jan 2025 00:00:00 GMT
```

---

## Webhook (オプション)

特定のイベント発生時にクライアントへ通知

### イベント一覧

| イベント | 説明 |
|---------|------|
| post.created | 投稿が作成された |
| post.published | 投稿が公開された |
| comment.created | コメントが作成された |
| user.registered | ユーザーが登録された |

### Webhook ペイロード例

```json
{
  "event": "post.published",
  "timestamp": "2024-01-01T12:00:00Z",
  "data": {
    "post_id": "660e8400-e29b-41d4-a716-446655440000",
    "title": "My Post",
    "author_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

---

## API変更履歴

| バージョン | 日付 | 変更内容 |
|----------|------|---------|
| v1.0.0 | [YYYY-MM-DD] | 初回リリース |
| v1.1.0 | [YYYY-MM-DD] | タグ機能追加 |
| v1.2.0 | [YYYY-MM-DD] | 検索機能強化 |
