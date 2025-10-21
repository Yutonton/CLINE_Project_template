# セキュリティポリシー

プロジェクトのセキュリティ方針と実装基準を定義します。

## 概要

このドキュメントでは、セキュリティリスクを最小化するための方針と実装ガイドラインを明確にします。

---

## 認証・認可

### パスワード

- **最小長**: 8文字
- **複雑性**: 英大小文字・数字・記号を含む
- **ハッシュ化**: bcrypt (コスト: 12以上)
- **保存禁止**: 平文パスワードの保存は禁止

### JWT

- **有効期限**: Access Token 1時間、Refresh Token 30日
- **シークレット**: 最低32文字の強力なランダム文字列
- **保存**: httpOnly Cookie推奨

---

## 入力バリデーション

### サーバーサイド

```typescript
// ✅ 必須: サーバーサイドでのバリデーション
app.post('/api/users', (req, res) => {
  const { email, password } = req.body;
  
  if (!isValidEmail(email)) {
    return res.status(400).json({ error: 'Invalid email' });
  }
  
  if (!isStrongPassword(password)) {
    return res.status(400).json({ error: 'Weak password' });
  }
  
  // 処理続行
});
```

---

## SQL インジェクション対策

```python
# ✅ プリペアドステートメント使用
cursor.execute("SELECT * FROM users WHERE email = ?", (email,))

# ❌ 文字列結合（危険）
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

---

## XSS対策

```typescript
// ✅ エスケープ処理
function escapeHtml(text: string): string {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;');
}

// Reactは自動エスケープ
<div>{userInput}</div>

// ❌ dangerouslySetInnerHTML（必要な場合のみ）
<div dangerouslySetInnerHTML={{ __html: sanitizedHtml }} />
```

---

## CSRF対策

- CSRFトークン使用
- SameSite Cookie属性設定

---

## HTTPS

- 本番環境では必須
- TLS 1.2以上

---

## 機密情報管理

### 環境変数

```bash
# .env (gitignore対象)
DATABASE_URL=postgresql://...
JWT_SECRET=...
API_KEY=...
```

### シークレット管理

- AWS Secrets Manager
- Azure Key Vault
- Google Cloud Secret Manager

---

## レート制限

```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/login")
@limiter.limit("5/15minute")
async def login():
    pass
```

---

## セキュリティヘッダー

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
```

---

## 脆弱性対応

### 依存関係

```bash
# 定期的な脆弱性スキャン
npm audit
pip-audit
```

### セキュリティアップデート

- 重大度高: 24時間以内
- 重大度中: 1週間以内
- 重大度低: 1ヶ月以内

---

## 更新履歴

| 日付 | 変更内容 | 更新者 |
|-----|---------|--------|
| [YYYY-MM-DD] | [変更内容] | [更新者] |
