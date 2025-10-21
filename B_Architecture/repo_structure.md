# リポジトリ構造

プロジェクトのリポジトリ構造とディレクトリ構成を定義します。

## 概要

このドキュメントでは、リポジトリ全体の構成、各ディレクトリの役割、ファイル命名規則、およびプロジェクト構造のベストプラクティスを明確にします。

---

## プロジェクト全体構造

```
project-root/
├── .github/                    # GitHub設定（Actions, Issue/PRテンプレート等）
│   └── workflows/              # GitHub Actions ワークフロー
├── .vscode/                    # VSCode設定
├── A_Requirements/             # 要件定義ドキュメント
├── B_Architecture/             # アーキテクチャ設計ドキュメント
├── C_DataModel/               # データモデルドキュメント
├── D_API/                     # API設計ドキュメント
├── E_UI/                      # UI設計ドキュメント
├── F_App/                     # アプリケーション実装
│   ├── frontend/              # フロントエンドコード
│   └── backend/               # バックエンドコード
├── G_Management/              # プロジェクト管理ドキュメント
├── rules/                     # 開発ルール・ガイドライン
├── tests/                     # テストコード
│   ├── auto_validation/       # 自動検証スクリプト
│   ├── e2e/                   # E2Eテスト（追加予定）
│   └── integration/           # 統合テスト（追加予定）
├── docs/                      # その他のドキュメント（追加予定）
├── scripts/                   # ユーティリティスクリプト（追加予定）
├── .gitignore                 # Git除外設定
├── README.md                  # プロジェクト概要
├── docker-compose.yml         # ローカル開発環境（追加予定）
└── Makefile                   # 共通タスクの自動化（追加予定）
```

---

## ディレクトリ詳細

### A_Requirements/ - 要件定義

プロジェクトの要件を定義するドキュメント群

```
A_Requirements/
├── overview.md                 # プロジェクト概要
├── functional_nonfunctional.md # 機能要件・非機能要件
└── user_stories.md            # ユーザーストーリー
```

**目的**: プロジェクトの目標、ターゲットユーザー、必要な機能を明確化

**更新頻度**: 要件変更時、新機能追加時

---

### B_Architecture/ - アーキテクチャ設計

システムの全体設計を記述するドキュメント群

```
B_Architecture/
├── tech_stack.md              # 技術スタック
├── repo_structure.md          # リポジトリ構造（このファイル）
└── infra_architecture.md      # インフラ構成
```

**目的**: 技術選定の根拠、システム構成、インフラ設計の可視化

**更新頻度**: 技術スタック変更時、アーキテクチャ見直し時

---

### C_DataModel/ - データモデル

データ構造とエンティティ関係を定義

```
C_DataModel/
├── entity_relation.md         # エンティティ関連図
└── db_schema.md              # データベーススキーマ
```

**目的**: データ構造の統一、テーブル設計の明確化

**更新頻度**: データモデル変更時、新エンティティ追加時

---

### D_API/ - API設計

APIの仕様と設計を定義

```
D_API/
├── endpoints.md               # エンドポイント定義
├── data_flow.md              # データフロー
└── api_authentication.md     # 認証設計
```

**目的**: API仕様の統一、フロントエンドとバックエンドの連携明確化

**更新頻度**: API追加・変更時

---

### E_UI/ - UI設計

ユーザーインターフェースの設計

```
E_UI/
├── screen_list.md            # 画面一覧
├── component_spec.md         # コンポーネント仕様
└── design_guideline_ref.md   # デザインガイドライン参照
```

**目的**: UI/UXの統一、コンポーネント設計の明確化

**更新頻度**: 画面追加・変更時、デザインシステム更新時

---

### F_App/ - アプリケーション実装

実際のソースコード

#### F_App/frontend/ - フロントエンド

```
F_App/frontend/
├── public/                    # 静的ファイル
│   ├── index.html
│   ├── favicon.ico
│   └── assets/               # 画像、フォント等
├── src/
│   ├── components/           # 再利用可能なコンポーネント
│   │   ├── common/          # 共通コンポーネント
│   │   ├── layout/          # レイアウトコンポーネント
│   │   └── features/        # 機能別コンポーネント
│   ├── pages/               # ページコンポーネント
│   ├── hooks/               # カスタムフック
│   ├── contexts/            # Context API
│   ├── services/            # API通信・外部サービス
│   ├── utils/               # ユーティリティ関数
│   ├── types/               # TypeScript型定義
│   ├── styles/              # グローバルスタイル
│   ├── constants/           # 定数定義
│   ├── routes/              # ルーティング設定
│   ├── store/               # 状態管理（Redux等）
│   ├── App.tsx              # ルートコンポーネント
│   └── index.tsx            # エントリーポイント
├── tests/                    # テストコード
│   ├── unit/                # 単体テスト
│   ├── integration/         # 統合テスト
│   └── e2e/                 # E2Eテスト
├── .env.example             # 環境変数サンプル
├── .eslintrc.js             # ESLint設定
├── .prettierrc              # Prettier設定
├── tsconfig.json            # TypeScript設定
├── vite.config.ts           # Vite設定（またはwebpack.config.js）
├── package.json             # 依存関係
└── README.md                # フロントエンド固有の説明
```

**命名規則**:
- コンポーネント: PascalCase (`UserProfile.tsx`)
- Hook: camelCase + use prefix (`useAuth.ts`)
- ユーティリティ: camelCase (`formatDate.ts`)
- 定数: UPPER_SNAKE_CASE (`API_BASE_URL`)
- CSS/Styles: kebab-case またはコンポーネント名に合わせる

---

#### F_App/backend/ - バックエンド

```
F_App/backend/
├── src/
│   ├── api/                 # APIエンドポイント
│   │   ├── v1/             # APIバージョン
│   │   │   ├── users/      # ユーザー関連エンドポイント
│   │   │   ├── auth/       # 認証関連エンドポイント
│   │   │   └── ...         # その他のリソース
│   │   └── dependencies.py  # 共通依存関係
│   ├── models/             # データモデル（ORM）
│   ├── schemas/            # Pydantic スキーマ（バリデーション）
│   ├── services/           # ビジネスロジック
│   ├── repositories/       # データアクセス層
│   ├── middleware/         # ミドルウェア
│   ├── core/               # コア機能
│   │   ├── config.py       # 設定管理
│   │   ├── security.py     # セキュリティ関連
│   │   └── database.py     # DB接続
│   ├── utils/              # ユーティリティ関数
│   ├── constants/          # 定数定義
│   ├── exceptions/         # カスタム例外
│   └── main.py             # アプリケーションエントリーポイント
├── tests/                  # テストコード
│   ├── unit/              # 単体テスト
│   ├── integration/       # 統合テスト
│   └── conftest.py        # pytest設定
├── migrations/            # DBマイグレーション（Alembic等）
├── scripts/               # ユーティリティスクリプト
├── .env.example          # 環境変数サンプル
├── .pylintrc             # Pylint設定
├── pyproject.toml        # Poetry設定（またはsetup.py）
├── requirements.txt       # 依存関係
├── Dockerfile            # Docker設定
└── README.md             # バックエンド固有の説明
```

**命名規則**:
- モジュール: snake_case (`user_service.py`)
- クラス: PascalCase (`UserService`)
- 関数: snake_case (`get_user_by_id`)
- 定数: UPPER_SNAKE_CASE (`MAX_LOGIN_ATTEMPTS`)
- プライベート: アンダースコアprefix (`_internal_function`)

---

### G_Management/ - プロジェクト管理

プロジェクトの進行管理に関するドキュメント

```
G_Management/
├── tasklist.md               # タスク一覧
├── schedule.md              # スケジュール
└── delivery_checklist.md    # デリバリーチェックリスト
```

**目的**: タスク管理、進捗追跡、リリース管理

**更新頻度**: 日次〜週次

---

### rules/ - 開発ルール

開発時に遵守すべきルールとガイドライン

```
rules/
├── coding_standard.md        # コーディング規約
├── design_guideline.md       # デザインガイドライン
├── security_policy.md        # セキュリティポリシー
├── validation_rule.md        # バリデーションルール
└── ai_generation.md          # AI生成ガイドライン
```

**目的**: コード品質の統一、セキュリティ確保

**更新頻度**: ルール追加・変更時

---

### tests/ - テスト

プロジェクト全体のテストコード

```
tests/
├── auto_validation/          # ドキュメント・コード整合性チェック
│   ├── consistency_check.py  # 整合性チェック
│   ├── naming_rule_test.py   # 命名規則テスト
│   └── schema_check.py       # スキーマ整合性チェック
├── e2e/                      # E2Eテスト
├── integration/              # 統合テスト
├── performance/              # パフォーマンステスト
└── security/                 # セキュリティテスト
```

**目的**: 品質保証、自動テスト

**更新頻度**: 機能追加時、バグ修正時

---

## ファイル命名規則

### 一般的なルール

1. **明確で説明的な名前を使用**
   - ❌ `data.json`
   - ✅ `user_profile_data.json`

2. **一貫性のある命名規則**
   - JavaScript/TypeScript: camelCase, PascalCase
   - Python: snake_case, PascalCase (クラス)
   - ファイル: kebab-case または snake_case

3. **省略形を避ける**
   - ❌ `usr_mgr.py`
   - ✅ `user_manager.py`

4. **バージョン管理が必要なファイル**
   - `api/v1/`, `api/v2/` のようにディレクトリでバージョン管理

### 特殊ファイル

| ファイル | 用途 |
|---------|------|
| `README.md` | プロジェクト/ディレクトリの説明 |
| `.env.example` | 環境変数のサンプル |
| `.gitignore` | Git除外設定 |
| `Dockerfile` | Docker設定 |
| `docker-compose.yml` | Docker Compose設定 |
| `Makefile` | タスク自動化 |
| `package.json` | Node.js依存関係 |
| `requirements.txt` | Python依存関係 |
| `tsconfig.json` | TypeScript設定 |
| `pytest.ini` | pytest設定 |

---

## ブランチ戦略

### Git Flow

```
main (本番環境)
  ↑
develop (開発環境)
  ↑
feature/* (機能開発)
hotfix/* (緊急修正)
release/* (リリース準備)
```

### ブランチ命名規則

| ブランチタイプ | 命名規則 | 例 |
|--------------|---------|-----|
| 機能開発 | `feature/[issue-number]-[feature-name]` | `feature/123-user-authentication` |
| バグ修正 | `fix/[issue-number]-[bug-description]` | `fix/456-login-error` |
| ホットフィックス | `hotfix/[issue-number]-[description]` | `hotfix/789-security-patch` |
| リリース | `release/[version]` | `release/v1.2.0` |

---

## コミットメッセージ規約

### Conventional Commits

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type

| Type | 説明 |
|------|------|
| `feat` | 新機能 |
| `fix` | バグ修正 |
| `docs` | ドキュメント変更 |
| `style` | コードフォーマット（機能変更なし） |
| `refactor` | リファクタリング |
| `test` | テスト追加・修正 |
| `chore` | ビルド・設定変更 |
| `perf` | パフォーマンス改善 |

### 例

```
feat(auth): add JWT authentication

Implement JWT-based authentication system with refresh tokens.
Includes middleware for token validation.

Closes #123
```

---

## 環境別設定

### 環境の種類

| 環境 | 説明 | ブランチ | URL例 |
|-----|------|---------|-------|
| Development | ローカル開発 | feature/* | `localhost:3000` |
| Staging | テスト環境 | develop | `staging.example.com` |
| Production | 本番環境 | main | `example.com` |

### 環境変数管理

```
.env.local          # ローカル開発用（gitignore）
.env.development    # 開発環境用
.env.staging        # ステージング環境用
.env.production     # 本番環境用
.env.example        # サンプル（必須項目を記載）
```

---

## ディレクトリ追加のガイドライン

新しいディレクトリを追加する際の基準：

1. **目的の明確化**: ディレクトリの役割を明確に定義
2. **README.md の配置**: 各主要ディレクトリにREADME.mdを配置
3. **命名の一貫性**: 既存の命名規則に従う
4. **最小限の階層**: 不必要にネストしない（3-4階層まで）

---

## 依存関係管理

### フロントエンド

- `package.json`: すべての依存関係を記載
- `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml`: バージョンロック

### バックエンド

- `requirements.txt`: 本番依存関係
- `requirements-dev.txt`: 開発依存関係
- または `pyproject.toml` (Poetry使用時)

---

## ドキュメント管理

### ドキュメントの種類

| 種類 | 場所 | 更新頻度 |
|-----|------|---------|
| 要件定義 | `A_Requirements/` | 要件変更時 |
| 設計書 | `B_Architecture/`, `C_DataModel/`, etc. | 設計変更時 |
| APIドキュメント | `D_API/` + 自動生成 | API変更時 |
| コードドキュメント | ソースコード内のコメント | 実装時 |
| README | 各ディレクトリ | 構造変更時 |

---

## ベストプラクティス

1. **単一責任の原則**: 各ファイル・ディレクトリは単一の責任を持つ
2. **関心の分離**: UI、ビジネスロジック、データアクセスを分離
3. **再利用性**: 共通機能は共通ディレクトリに配置
4. **テスト容易性**: テストしやすい構造を維持
5. **ドキュメント化**: コードと並行してドキュメントを更新

---

## リポジトリ構造の更新履歴

| 日付 | 変更内容 | 理由 | 担当者 |
|-----|---------|------|--------|
| [YYYY-MM-DD] | [変更内容] | [理由] | [担当者] |
