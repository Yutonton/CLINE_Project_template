# PRD テンプレート（CLINE + Checkpoint 運用）

このテンプレートは、CLINEを活用したアプリケーション開発において、要件定義からアーキテクチャ設計、実装、テストまで一貫した開発を行うための包括的なドキュメント構造を提供します。

## 📁 ディレクトリ構成

```
CLINE_Project_template/
├── A_Requirements/          # 要件定義
│   ├── overview.md         # プロジェクト概要
│   ├── functional_nonfunctional.md  # 機能要件・非機能要件
│   └── user_stories.md     # ユーザーストーリー
├── B_Architecture/         # アーキテクチャ設計
│   ├── tech_stack.md       # 技術スタック
│   ├── repo_structure.md   # リポジトリ構造
│   └── infra_architecture.md  # インフラ構成
├── C_DataModel/            # データモデル
│   ├── entity_relation.md  # エンティティ関連図
│   └── db_schema.md        # データベーススキーマ
├── D_API/                  # API設計
│   ├── endpoints.md        # エンドポイント定義
│   ├── data_flow.md        # データフロー
│   └── api_authentication.md  # 認証設計
├── E_UI/                   # UI設計
│   ├── screen_list.md      # 画面一覧
│   ├── component_spec.md   # コンポーネント仕様
│   └── design_guideline_ref.md  # デザインガイドライン参照
├── F_App/                  # アプリケーション実装
│   ├── frontend/           # フロントエンド
│   └── backend/            # バックエンド
├── G_Management/           # プロジェクト管理
│   ├── tasklist.md         # タスク一覧
│   ├── schedule.md         # スケジュール
│   └── delivery_checklist.md  # デリバリーチェックリスト
├── rules/                  # 開発ルール
│   ├── coding_standard.md  # コーディング規約
│   ├── design_guideline.md # デザインガイドライン
│   ├── security_policy.md  # セキュリティポリシー
│   ├── validation_rule.md  # バリデーションルール
│   └── ai_generation.md    # AI生成ガイドライン
└── tests/                  # テスト
    └── auto_validation/    # 自動検証スクリプト
```

## 🚀 使い方

### 1. テンプレートの初期化

1. このテンプレートをクローンまたはコピーします
2. プロジェクト名に合わせてルートディレクトリ名を変更します
3. 各ドキュメントを要件に応じて記入していきます

### 2. ドキュメントの記入順序

推奨される記入順序：

1. **A_Requirements/** - 要件定義から開始
   - `overview.md`: プロジェクトの目的と背景を明確化
   - `functional_nonfunctional.md`: 機能要件と非機能要件を定義
   - `user_stories.md`: ユーザー視点での機能を記述

2. **B_Architecture/** - アーキテクチャを設計
   - `tech_stack.md`: 使用する技術スタックを決定
   - `repo_structure.md`: リポジトリの構成を設計
   - `infra_architecture.md`: インフラ構成を計画

3. **C_DataModel/** - データ構造を定義
   - `entity_relation.md`: エンティティ関連図を作成
   - `db_schema.md`: データベーススキーマを定義

4. **D_API/** - APIを設計
   - `endpoints.md`: APIエンドポイントを定義
   - `data_flow.md`: データの流れを図示
   - `api_authentication.md`: 認証方式を設計

5. **E_UI/** - UI設計
   - `screen_list.md`: 画面一覧を作成
   - `component_spec.md`: コンポーネント仕様を定義
   - `design_guideline_ref.md`: デザインガイドラインを参照

6. **rules/** - 開発ルールを整備
   - 各ルールファイルをプロジェクトに合わせて調整

7. **F_App/** - 実装開始
   - ドキュメントに基づいて実装を進める

8. **G_Management/** - プロジェクト管理
   - タスク管理とスケジュール管理を行う

### 3. CLINE との連携

このテンプレートは、CLINEのCheckpoint機能と組み合わせて使用することを想定しています：

- 各フェーズの完了時にCheckpointを作成
- ドキュメントの変更履歴を追跡
- AI生成コードとの一貫性を保持

### 4. 自動検証

`tests/auto_validation/` には、ドキュメント間の整合性やルール遵守を自動でチェックするスクリプトが含まれています：

```bash
# 整合性チェック
python tests/auto_validation/consistency_check.py

# 命名規則チェック
python tests/auto_validation/naming_rule_test.py

# スキーマ整合性チェック
python tests/auto_validation/schema_check.py
```

## 📝 注意事項

- 各ドキュメントには、記入例やテンプレートが含まれています
- プロジェクトの規模に応じて、不要なドキュメントは削除してもかまいません
- ドキュメントは継続的に更新し、実装との整合性を保ってください
- 特定のライブラリやフレームワークに依存しない設計になっているため、プロジェクトに応じて柔軟にカスタマイズしてください

## 🔧 開発環境

- **フロントエンド**: `F_App/frontend/` - 技術スタックは要件に応じて選択
- **バックエンド**: `F_App/backend/` - 技術スタックは要件に応じて選択
- **テスト**: `tests/` - 自動検証スクリプトとテストコード

## 📚 参考資料

- 各ドキュメント内に具体的な記入例とガイドラインが含まれています
- `rules/` ディレクトリに開発時の各種ルールが定義されています

## ライセンス

このテンプレートは自由に使用・改変できます。
