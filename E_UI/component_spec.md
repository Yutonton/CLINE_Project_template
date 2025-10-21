# コンポーネント仕様

再利用可能なUIコンポーネントの仕様を定義します。

## 概要

このドキュメントでは、アプリケーション全体で使用する共通コンポーネントの仕様と使用方法を明確にします。

---

## コンポーネント一覧

| コンポーネント名 | カテゴリー | 説明 | 優先度 |
|---------------|----------|------|--------|
| Button | Basic | ボタン | 高 |
| Input | Form | 入力フィールド | 高 |
| Card | Layout | カード | 高 |
| Modal | Overlay | モーダルダイアログ | 高 |
| Header | Layout | ヘッダー | 高 |
| Footer | Layout | フッター | 中 |
| Pagination | Navigation | ページネーション | 中 |
| Toast | Feedback | 通知メッセージ | 中 |
| Dropdown | Form | ドロップダウン | 中 |
| Avatar | Display | アバター画像 | 低 |

---

## 基本コンポーネント

### Button

**説明**: クリック可能なボタンコンポーネント

**Props**:
```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger' | 'text';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  loading?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}
```

**バリエーション**:
- **Primary**: メインアクション用（例: 保存、送信）
- **Secondary**: サブアクション用（例: キャンセル）
- **Danger**: 削除など注意が必要なアクション
- **Text**: テキストリンクスタイル

**使用例**:
```tsx
<Button variant="primary" size="medium" onClick={handleSubmit}>
  送信
</Button>
```

---

### Input

**説明**: テキスト入力フィールド

**Props**:
```typescript
interface InputProps {
  type?: 'text' | 'email' | 'password' | 'number';
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  error?: string;
  disabled?: boolean;
  required?: boolean;
}
```

**状態**:
- Default
- Focus
- Error
- Disabled

**使用例**:
```tsx
<Input
  type="email"
  value={email}
  onChange={setEmail}
  placeholder="メールアドレス"
  error={emailError}
  required
/>
```

---

### Card

**説明**: コンテンツをグループ化するカード

**Props**:
```typescript
interface CardProps {
  title?: string;
  footer?: React.ReactNode;
  children: React.ReactNode;
  onClick?: () => void;
}
```

**使用例**:
```tsx
<Card title="投稿タイトル" footer={<PostMeta />}>
  <p>投稿内容...</p>
</Card>
```

---

## レイアウトコンポーネント

### Header

**説明**: アプリケーションヘッダー

**Props**:
```typescript
interface HeaderProps {
  user?: User;
  onLogout?: () => void;
}
```

**構成要素**:
- ロゴ
- ナビゲーションメニュー
- ユーザーメニュー（ログイン時）
- ログイン/登録ボタン（未ログイン時）

---

### Modal

**説明**: モーダルダイアログ

**Props**:
```typescript
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}
```

**使用例**:
```tsx
<Modal
  isOpen={isOpen}
  onClose={handleClose}
  title="確認"
  footer={
    <>
      <Button variant="secondary" onClick={handleClose}>キャンセル</Button>
      <Button variant="danger" onClick={handleDelete}>削除</Button>
    </>
  }
>
  <p>本当に削除しますか？</p>
</Modal>
```

---

## フォームコンポーネント

### Form

**説明**: フォーム全体のラッパー

**Props**:
```typescript
interface FormProps {
  onSubmit: (data: FormData) => void;
  children: React.ReactNode;
}
```

---

### Textarea

**説明**: 複数行テキスト入力

**Props**:
```typescript
interface TextareaProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  rows?: number;
  maxLength?: number;
}
```

---

## フィードバックコンポーネント

### Toast

**説明**: 一時的な通知メッセージ

**Props**:
```typescript
interface ToastProps {
  message: string;
  type?: 'success' | 'error' | 'info' | 'warning';
  duration?: number;
  onClose?: () => void;
}
```

**表示位置**: 画面右上

**表示時間**: 3秒（デフォルト）

---

### Loading

**説明**: ローディングインジケーター

**バリエーション**:
- Spinner（小・中・大）
- Skeleton Screen
- Progress Bar

---

## ナビゲーションコンポーネント

### Pagination

**説明**: ページネーション

**Props**:
```typescript
interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}
```

---

## 表示コンポーネント

### Avatar

**説明**: ユーザーアバター

**Props**:
```typescript
interface AvatarProps {
  src?: string;
  alt: string;
  size?: 'small' | 'medium' | 'large';
  fallback?: string; // イニシャルなど
}
```

---

### Badge

**説明**: ステータスバッジ

**Props**:
```typescript
interface BadgeProps {
  text: string;
  variant?: 'primary' | 'secondary' | 'success' | 'danger';
}
```

---

## コンポーネント設計原則

1. **単一責任の原則**: 1つのコンポーネントは1つの責任のみ
2. **再利用性**: プロジェクト全体で再利用可能に
3. **カスタマイズ性**: Props で柔軟にカスタマイズ可能
4. **アクセシビリティ**: ARIA属性の適切な使用
5. **型安全性**: TypeScript で厳密に型定義

---

## スタイリング方針

### CSS Modules / Styled Components / Tailwind CSS

プロジェクトに応じて選択

**例: CSS Modules**
```tsx
import styles from './Button.module.css';

<button className={styles.button}>Click</button>
```

---

## テスト

### 単体テスト

```typescript
describe('Button', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    fireEvent.click(screen.getByText('Click'));
    expect(handleClick).toHaveBeenCalled();
  });
});
```

---

## Storybook

コンポーネントカタログとして Storybook を使用

```typescript
export default {
  title: 'Components/Button',
  component: Button,
};

export const Primary = () => <Button variant="primary">Primary Button</Button>;
export const Secondary = () => <Button variant="secondary">Secondary</Button>;
```

---

## 更新履歴

| 日付 | 変更内容 | 担当者 |
|-----|---------|--------|
| [YYYY-MM-DD] | [変更内容] | [担当者] |
