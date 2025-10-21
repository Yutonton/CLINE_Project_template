# バリデーションルール

入力データの検証ルールを定義します。

## 概要

データの整合性とセキュリティを保つためのバリデーションルールです。

---

## 共通ルール

### 必須チェック

```typescript
if (!value || value.trim() === '') {
  throw new ValidationError('This field is required');
}
```

### 文字列長

```typescript
if (value.length < min || value.length > max) {
  throw new ValidationError(`Length must be between ${min} and ${max}`);
}
```

---

## ユーザー入力

### メールアドレス

- **形式**: RFC 5322準拠
- **最大長**: 255文字
- **重複**: 不可

```typescript
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
if (!emailRegex.test(email)) {
  throw new ValidationError('Invalid email format');
}
```

### パスワード

- **最小長**: 8文字
- **最大長**: 128文字
- **複雑性**: 英大小文字・数字・記号を含む

```typescript
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
```

### 表示名

- **最小長**: 1文字
- **最大長**: 100文字
- **許可文字**: 英数字、日本語、一部記号

---

## 投稿

### タイトル

- **必須**: Yes
- **最小長**: 1文字
- **最大長**: 255文字

### 本文

- **必須**: Yes
- **最小長**: 1文字
- **最大長**: 50,000文字

### タグ

- **必須**: No
- **最大数**: 5個
- **各タグ最大長**: 50文字
- **形式**: 英数字とハイフン

---

## API入力

### ページネーション

```typescript
page: number (min: 1, default: 1)
per_page: number (min: 1, max: 100, default: 20)
```

### UUID

```typescript
const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
```

---

## ファイルアップロード

### 画像

- **形式**: JPEG, PNG, GIF, WebP
- **最大サイズ**: 5MB
- **最大解像度**: 4000x4000px

```typescript
const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
const maxSize = 5 * 1024 * 1024; // 5MB
```

---

## 更新履歴

| 日付 | 変更内容 | 更新者 |
|-----|---------|--------|
| [YYYY-MM-DD] | [変更内容] | [更新者] |
