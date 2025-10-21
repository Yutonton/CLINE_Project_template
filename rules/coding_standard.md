# コーディング規約

プロジェクトのコーディング標準を定義します。

## 概要

このドキュメントでは、コードの一貫性と可読性を保つためのコーディング規約を明確にします。

---

## 一般原則

1. **可読性**: コードは書くよりも読まれることが多い
2. **一貫性**: プロジェクト全体で統一されたスタイル
3. **シンプルさ**: 複雑さを避け、シンプルに保つ
4. **DRY原則**: Don't Repeat Yourself（繰り返しを避ける）
5. **SOLID原則**: オブジェクト指向設計の5原則

---

## 命名規則

### JavaScript/TypeScript

```typescript
// クラス: PascalCase
class UserService {}

// 関数・変数: camelCase
function getUserById(userId: string) {}
const userName = 'John';

// 定数: UPPER_SNAKE_CASE
const API_BASE_URL = 'https://api.example.com';

// プライベート: _prefix
class MyClass {
  private _internalValue: number;
}

// インターフェース: PascalCase (Iプレフィックスなし)
interface User {
  id: string;
  name: string;
}

// Type: PascalCase
type UserRole = 'admin' | 'user';
```

### Python

```python
# クラス: PascalCase
class UserService:
    pass

# 関数・変数: snake_case
def get_user_by_id(user_id: str):
    pass

user_name = "John"

# 定数: UPPER_SNAKE_CASE
API_BASE_URL = "https://api.example.com"

# プライベート: _prefix
class MyClass:
    def __init__(self):
        self._internal_value = 0
```

---

## ファイル構成

### フロントエンド（TypeScript/React）

```typescript
// 1. Import文（外部ライブラリ→内部モジュール）
import React, { useState, useEffect } from 'react';
import axios from 'axios';

import { Button } from '@/components/Button';
import { useAuth } from '@/hooks/useAuth';
import type { User } from '@/types/user';

// 2. 型定義
interface Props {
  userId: string;
}

// 3. コンポーネント定義
export const UserProfile: React.FC<Props> = ({ userId }) => {
  // 4. State
  const [user, setUser] = useState<User | null>(null);
  
  // 5. Hooks
  const { token } = useAuth();
  
  // 6. Effect
  useEffect(() => {
    // ...
  }, [userId]);
  
  // 7. ハンドラー
  const handleUpdate = () => {
    // ...
  };
  
  // 8. レンダリング
  return (
    <div>
      {/* ... */}
    </div>
  );
};
```

### バックエンド（Python/FastAPI）

```python
# 1. 標準ライブラリ
from datetime import datetime
from typing import Optional

# 2. サードパーティライブラリ
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# 3. 内部モジュール
from app.models import User
from app.schemas import UserCreate, UserResponse
from app.dependencies import get_db

# 4. ルーター定義
router = APIRouter()

# 5. エンドポイント定義
@router.post("/users", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """ユーザーを作成する"""
    # ...
```

---

## コメント

### 良いコメント

```typescript
// ✅ なぜそうするのかを説明
// 認証トークンの有効期限を延長するため、5分前に更新
if (tokenExpiresIn < 300) {
  refreshToken();
}

// ✅ 複雑なロジックの説明
// Fisher-Yatesアルゴリズムで配列をシャッフル
function shuffle(array: any[]) {
  // ...
}
```

### 避けるべきコメント

```typescript
// ❌ コードそのものを説明（自明）
// ユーザー名を設定
const userName = 'John';

// ❌ 不要なコメント
// ループ
for (let i = 0; i < 10; i++) {
  // ...
}
```

---

## 関数・メソッド

### 原則

- **単一責任**: 1つの関数は1つのことだけを行う
- **短く**: 20行以内が望ましい
- **引数**: 3個以内が望ましい

### 例

```typescript
// ✅ 良い例
function calculateTotal(price: number, quantity: number): number {
  return price * quantity;
}

// ❌ 悪い例（複数の責任）
function processOrder(order: Order) {
  // 在庫チェック
  // 価格計算
  // メール送信
  // DB更新
  // ...
}
```

---

## エラーハンドリング

```typescript
// ✅ 適切なエラーハンドリング
async function fetchUser(id: string): Promise<User> {
  try {
    const response = await api.get(`/users/${id}`);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.response?.status === 404) {
        throw new UserNotFoundError(id);
      }
    }
    throw new UnexpectedError('Failed to fetch user', error);
  }
}

// ❌ 空のcatch（エラーを無視）
try {
  // ...
} catch (error) {
  // 何もしない
}
```

---

## 非同期処理

```typescript
// ✅ async/await使用
async function fetchData() {
  const user = await getUser();
  const posts = await getPosts(user.id);
  return { user, posts };
}

// ❌ Promiseチェーン（可読性低い）
function fetchData() {
  return getUser()
    .then(user => getPosts(user.id)
      .then(posts => ({ user, posts })));
}
```

---

## テスト

```typescript
// テストの構造: AAA (Arrange, Act, Assert)
describe('UserService', () => {
  describe('createUser', () => {
    it('should create a new user', async () => {
      // Arrange
      const userData = { email: 'test@example.com', name: 'Test User' };
      
      // Act
      const user = await userService.createUser(userData);
      
      // Assert
      expect(user.email).toBe(userData.email);
      expect(user.id).toBeDefined();
    });
  });
});
```

---

## Linter/Formatter設定

### ESLint (.eslintrc.js)

```javascript
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/recommended',
    'prettier'
  ],
  rules: {
    'no-console': 'warn',
    'no-unused-vars': 'error',
    '@typescript-eslint/explicit-function-return-type': 'warn'
  }
};
```

### Prettier (.prettierrc)

```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "es5",
  "printWidth": 100,
  "tabWidth": 2
}
```

---

## Git コミットメッセージ

### フォーマット

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type

- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメント変更
- `style`: フォーマット変更
- `refactor`: リファクタリング
- `test`: テスト追加
- `chore`: ビルド・設定変更

### 例

```
feat(auth): add JWT authentication

Implement JWT-based authentication with refresh tokens.
Includes middleware for token validation.

Closes #123
```

---

## 更新履歴

| 日付 | 変更内容 | 更新者 |
|-----|---------|--------|
| [YYYY-MM-DD] | [変更内容] | [更新者] |
