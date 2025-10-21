# データベーススキーマ

データベースの物理的なスキーマ定義とテーブル設計を記述します。

## 概要

このドキュメントでは、実際のデータベーステーブルの構造、制約、インデックス、パーティショニングなどの物理設計を定義します。

---

## データベース情報

| 項目 | 設定値 |
|-----|-------|
| データベース種類 | PostgreSQL 15.x |
| 文字コード | UTF-8 |
| タイムゾーン | UTC |
| 命名規則 | snake_case |

---

## テーブル定義

### users テーブル

**説明**: ユーザー情報を管理するテーブル

```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    last_login TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- インデックス
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at DESC);
CREATE INDEX idx_users_is_active ON users(is_active) WHERE is_active = TRUE;

-- コメント
COMMENT ON TABLE users IS 'ユーザー認証情報';
COMMENT ON COLUMN users.user_id IS 'ユーザーID（主キー）';
COMMENT ON COLUMN users.email IS 'メールアドレス（ログインID）';
COMMENT ON COLUMN users.password_hash IS 'パスワードハッシュ（bcrypt）';
```

---

### profiles テーブル

**説明**: ユーザーの公開プロフィール情報

```sql
CREATE TABLE profiles (
    profile_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(user_id) ON DELETE CASCADE,
    display_name VARCHAR(100) NOT NULL,
    bio TEXT,
    avatar_url VARCHAR(500),
    location VARCHAR(100),
    website VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_display_name_length CHECK (char_length(display_name) >= 1),
    CONSTRAINT chk_bio_length CHECK (bio IS NULL OR char_length(bio) <= 500)
);

-- インデックス
CREATE UNIQUE INDEX idx_profiles_user_id ON profiles(user_id);
CREATE INDEX idx_profiles_display_name ON profiles(display_name);

-- コメント
COMMENT ON TABLE profiles IS 'ユーザープロフィール情報';
```

---

### posts テーブル

**説明**: ユーザーが作成する投稿コンテンツ

```sql
CREATE TABLE posts (
    post_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    published_at TIMESTAMP WITH TIME ZONE,
    view_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_status CHECK (status IN ('draft', 'published', 'archived')),
    CONSTRAINT chk_published_at CHECK (
        (status = 'published' AND published_at IS NOT NULL) OR
        (status != 'published')
    )
);

-- インデックス
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_status_published_at ON posts(status, published_at DESC) 
    WHERE status = 'published';
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);
CREATE INDEX idx_posts_view_count ON posts(view_count DESC);

-- 全文検索インデックス
CREATE INDEX idx_posts_title_content_fts ON posts 
    USING gin(to_tsvector('english', title || ' ' || content));

-- コメント
COMMENT ON TABLE posts IS '投稿コンテンツ';
COMMENT ON COLUMN posts.status IS 'ステータス: draft/published/archived';
```

---

### comments テーブル

**説明**: 投稿に対するコメント

```sql
CREATE TABLE comments (
    comment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID NOT NULL REFERENCES posts(post_id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE SET NULL,
    parent_id UUID REFERENCES comments(comment_id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_content_length CHECK (char_length(content) >= 1 AND char_length(content) <= 5000),
    CONSTRAINT chk_no_self_parent CHECK (comment_id != parent_id)
);

-- インデックス
CREATE INDEX idx_comments_post_id ON comments(post_id);
CREATE INDEX idx_comments_user_id ON comments(user_id);
CREATE INDEX idx_comments_parent_id ON comments(parent_id) WHERE parent_id IS NOT NULL;
CREATE INDEX idx_comments_created_at ON comments(created_at DESC);

-- コメント
COMMENT ON TABLE comments IS '投稿へのコメント';
COMMENT ON COLUMN comments.parent_id IS '親コメントID（返信用）';
```

---

### tags テーブル

**説明**: 投稿の分類用タグ

```sql
CREATE TABLE tags (
    tag_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL UNIQUE,
    slug VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    usage_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_name_format CHECK (name ~* '^[a-z0-9-]+$'),
    CONSTRAINT chk_slug_format CHECK (slug ~* '^[a-z0-9-]+$')
);

-- インデックス
CREATE UNIQUE INDEX idx_tags_name ON tags(LOWER(name));
CREATE UNIQUE INDEX idx_tags_slug ON tags(slug);
CREATE INDEX idx_tags_usage_count ON tags(usage_count DESC);

-- コメント
COMMENT ON TABLE tags IS '投稿分類用タグ';
COMMENT ON COLUMN tags.slug IS 'URL用スラッグ（小文字英数字とハイフン）';
```

---

### post_tags テーブル

**説明**: 投稿とタグの多対多関連テーブル

```sql
CREATE TABLE post_tags (
    post_id UUID NOT NULL REFERENCES posts(post_id) ON DELETE CASCADE,
    tag_id UUID NOT NULL REFERENCES tags(tag_id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (post_id, tag_id)
);

-- インデックス
CREATE INDEX idx_post_tags_tag_id ON post_tags(tag_id);

-- コメント
COMMENT ON TABLE post_tags IS '投稿とタグの関連テーブル';
```

---

## トリガー定義

### 更新日時の自動更新

```sql
-- 更新日時を自動的にCURRENT_TIMESTAMPに更新する関数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- users テーブル用トリガー
CREATE TRIGGER trg_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- profiles テーブル用トリガー
CREATE TRIGGER trg_profiles_updated_at
    BEFORE UPDATE ON profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- posts テーブル用トリガー
CREATE TRIGGER trg_posts_updated_at
    BEFORE UPDATE ON posts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- comments テーブル用トリガー
CREATE TRIGGER trg_comments_updated_at
    BEFORE UPDATE ON comments
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### タグ使用回数の自動更新

```sql
-- タグ使用回数を更新する関数
CREATE OR REPLACE FUNCTION update_tag_usage_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE tags SET usage_count = usage_count + 1 WHERE tag_id = NEW.tag_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE tags SET usage_count = usage_count - 1 WHERE tag_id = OLD.tag_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- post_tags テーブル用トリガー
CREATE TRIGGER trg_post_tags_usage_count
    AFTER INSERT OR DELETE ON post_tags
    FOR EACH ROW
    EXECUTE FUNCTION update_tag_usage_count();
```

---

## ビュー定義

### 公開投稿一覧ビュー

```sql
CREATE VIEW v_published_posts AS
SELECT 
    p.post_id,
    p.user_id,
    u.email AS author_email,
    pr.display_name AS author_name,
    p.title,
    p.content,
    p.view_count,
    p.published_at,
    p.created_at,
    p.updated_at,
    COUNT(DISTINCT c.comment_id) AS comment_count,
    ARRAY_AGG(DISTINCT t.name) FILTER (WHERE t.name IS NOT NULL) AS tags
FROM posts p
LEFT JOIN users u ON p.user_id = u.user_id
LEFT JOIN profiles pr ON u.user_id = pr.user_id
LEFT JOIN comments c ON p.post_id = c.post_id AND c.is_deleted = FALSE
LEFT JOIN post_tags pt ON p.post_id = pt.post_id
LEFT JOIN tags t ON pt.tag_id = t.tag_id
WHERE p.status = 'published'
GROUP BY p.post_id, p.user_id, u.email, pr.display_name;

COMMENT ON VIEW v_published_posts IS '公開済み投稿の一覧（コメント数とタグを含む）';
```

### ユーザー統計ビュー

```sql
CREATE VIEW v_user_statistics AS
SELECT 
    u.user_id,
    u.email,
    pr.display_name,
    COUNT(DISTINCT p.post_id) AS post_count,
    COUNT(DISTINCT c.comment_id) AS comment_count,
    COALESCE(SUM(p.view_count), 0) AS total_views,
    MAX(p.published_at) AS last_post_date
FROM users u
LEFT JOIN profiles pr ON u.user_id = pr.user_id
LEFT JOIN posts p ON u.user_id = p.user_id AND p.status = 'published'
LEFT JOIN comments c ON u.user_id = c.user_id AND c.is_deleted = FALSE
GROUP BY u.user_id, u.email, pr.display_name;

COMMENT ON VIEW v_user_statistics IS 'ユーザーごとの統計情報';
```

---

## マイグレーション戦略

### バージョン管理

マイグレーションツール: **Alembic** (Python) または **TypeORM** (Node.js)

```
migrations/
├── versions/
│   ├── 001_initial_schema.sql
│   ├── 002_add_tags_table.sql
│   ├── 003_add_full_text_search.sql
│   └── ...
└── README.md
```

### マイグレーションルール

1. **下位互換性を保つ**: 既存データを壊さない
2. **段階的な変更**: 大きな変更は複数のマイグレーションに分割
3. **ロールバック可能**: すべてのマイグレーションにダウン処理を用意
4. **本番環境での実行前にステージングで検証**

### マイグレーション例

```sql
-- 001_initial_schema.sql (UP)
BEGIN;

CREATE TABLE users (...);
CREATE TABLE profiles (...);
-- ... 他のテーブル

COMMIT;

-- 001_initial_schema_down.sql (DOWN)
BEGIN;

DROP TABLE IF EXISTS profiles CASCADE;
DROP TABLE IF EXISTS users CASCADE;

COMMIT;
```

---

## パーティショニング

### posts テーブルのパーティショニング（オプション）

大量のデータが予想される場合、日付ベースのパーティショニングを検討

```sql
-- パーティションテーブルの作成
CREATE TABLE posts (
    -- ... カラム定義 ...
) PARTITION BY RANGE (created_at);

-- 月次パーティション例
CREATE TABLE posts_2024_01 PARTITION OF posts
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE posts_2024_02 PARTITION OF posts
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
```

---

## パフォーマンスチューニング

### PostgreSQL 設定

```sql
-- 接続設定
max_connections = 200

-- メモリ設定
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 128MB

-- クエリプランナー
random_page_cost = 1.1  -- SSD使用時
effective_io_concurrency = 200

-- ログ設定
log_min_duration_statement = 1000  -- 1秒以上かかるクエリをログ
```

### VACUUM とANALYZE

```sql
-- 定期的な自動バキューム設定
ALTER TABLE posts SET (autovacuum_vacuum_scale_factor = 0.1);
ALTER TABLE comments SET (autovacuum_vacuum_scale_factor = 0.1);

-- 手動実行（メンテナンス時）
VACUUM ANALYZE;
```

---

## データ整合性チェック

### 制約チェックスクリプト

```sql
-- 孤立したプロフィールのチェック
SELECT p.profile_id
FROM profiles p
LEFT JOIN users u ON p.user_id = u.user_id
WHERE u.user_id IS NULL;

-- 無効なコメント親参照のチェック
SELECT c1.comment_id
FROM comments c1
LEFT JOIN comments c2 ON c1.parent_id = c2.comment_id
WHERE c1.parent_id IS NOT NULL AND c2.comment_id IS NULL;

-- タグの使用回数不整合のチェック
SELECT t.tag_id, t.name, t.usage_count, COUNT(pt.post_id) AS actual_count
FROM tags t
LEFT JOIN post_tags pt ON t.tag_id = pt.tag_id
GROUP BY t.tag_id, t.name, t.usage_count
HAVING t.usage_count != COUNT(pt.post_id);
```

---

## バックアップとリストア

### バックアップコマンド

```bash
# フルバックアップ
pg_dump -h localhost -U postgres -d mydb -F c -f backup_$(date +%Y%m%d).dump

# スキーマのみバックアップ
pg_dump -h localhost -U postgres -d mydb --schema-only > schema.sql

# 特定テーブルのバックアップ
pg_dump -h localhost -U postgres -d mydb -t users -t profiles > users_backup.sql
```

### リストアコマンド

```bash
# フルリストア
pg_restore -h localhost -U postgres -d mydb backup_20240101.dump

# スキーマリストア
psql -h localhost -U postgres -d mydb < schema.sql
```

---

## セキュリティ

### ロールとパーミッション

```sql
-- アプリケーション用ロール
CREATE ROLE app_user WITH LOGIN PASSWORD 'secure_password';

-- 読み取り専用ロール
CREATE ROLE app_readonly WITH LOGIN PASSWORD 'secure_password';

-- 権限付与
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_readonly;

-- デフォルト権限設定
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_user;
```

### Row Level Security (RLS)

```sql
-- RLS有効化
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- ポリシー作成（例: ユーザーは自分の投稿のみ編集可能）
CREATE POLICY post_owner_policy ON posts
    FOR UPDATE
    USING (user_id = current_setting('app.current_user_id')::UUID);
```

---

## モニタリングクエリ

### スロークエリの確認

```sql
-- 実行中の長時間クエリ
SELECT 
    pid,
    now() - query_start AS duration,
    query,
    state
FROM pg_stat_activity
WHERE state != 'idle'
    AND now() - query_start > interval '30 seconds'
ORDER BY duration DESC;
```

### テーブルサイズの確認

```sql
-- テーブルサイズとインデックスサイズ
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) AS table_size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - 
                   pg_relation_size(schemaname||'.'||tablename)) AS index_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

---

## スキーマ更新履歴

| バージョン | 日付 | 変更内容 | 担当者 |
|----------|------|---------|--------|
| 1.0.0 | [YYYY-MM-DD] | 初期スキーマ作成 | [担当者] |
| 1.1.0 | [YYYY-MM-DD] | タグ機能追加 | [担当者] |
| 1.2.0 | [YYYY-MM-DD] | 全文検索インデックス追加 | [担当者] |
