# インフラストラクチャ構成

システムのインフラストラクチャ構成と運用設計を定義します。

## 概要

このドキュメントでは、システムのインフラ構成、デプロイメント戦略、スケーリング方針、監視・ログ管理、バックアップ・災害復旧計画を明確にします。

---

## システムアーキテクチャ概要

### 全体構成図

```
[ユーザー]
    ↓
[CDN / CloudFront]
    ↓
[Load Balancer / ALB]
    ↓
┌─────────────────────┬─────────────────────┐
│  Frontend           │  Backend            │
│  (Web Server)       │  (Application)      │
│  - React/Vue/etc    │  - API Server       │
│  - Nginx/CDN        │  - FastAPI/Express  │
└─────────────────────┴─────────────────────┘
         │                      │
         └──────────┬───────────┘
                    ↓
         ┌─────────────────────┐
         │  Cache Layer        │
         │  - Redis            │
         └─────────────────────┘
                    ↓
         ┌─────────────────────┐
         │  Database           │
         │  - PostgreSQL       │
         │  - Read Replica     │
         └─────────────────────┘
                    ↓
         ┌─────────────────────┐
         │  Object Storage     │
         │  - S3 / GCS / Blob  │
         └─────────────────────┘
```

---

## 環境構成

### 環境一覧

| 環境 | 目的 | URL | インフラ |
|-----|------|-----|---------|
| Development | ローカル開発 | `localhost` | Docker Compose |
| Staging | テスト・検証 | `staging.example.com` | [クラウドプロバイダー] |
| Production | 本番運用 | `example.com` | [クラウドプロバイダー] |

### 環境別リソース

| リソース | Development | Staging | Production |
|---------|------------|---------|-----------|
| Web Server | 1 instance | 2 instances | 4+ instances (Auto-scaling) |
| API Server | 1 instance | 2 instances | 4+ instances (Auto-scaling) |
| Database | 1 instance | 1 instance + replica | 1 primary + 2 replicas |
| Cache | 1 instance | 1 instance | 3 instances (cluster) |
| Storage | Local | Cloud Storage | Cloud Storage (multi-region) |

---

## ネットワーク構成

### ネットワーク図

```
Internet
    │
    ├─ [CDN] (静的コンテンツ配信)
    │
    └─ [WAF] (Web Application Firewall)
         ↓
    [Load Balancer]
         ↓
    ┌────────────────────┐
    │   Public Subnet    │
    │  - Web Servers     │
    │  - Bastion Host    │
    └────────────────────┘
         ↓
    ┌────────────────────┐
    │  Private Subnet    │
    │  - App Servers     │
    │  - Cache Servers   │
    └────────────────────┘
         ↓
    ┌────────────────────┐
    │  Data Subnet       │
    │  - Databases       │
    └────────────────────┘
```

### セキュリティグループ / ファイアウォールルール

#### Web Server (Public Subnet)

| Direction | Protocol | Port | Source | 説明 |
|-----------|----------|------|--------|------|
| Inbound | HTTP | 80 | 0.0.0.0/0 | HTTP通信 |
| Inbound | HTTPS | 443 | 0.0.0.0/0 | HTTPS通信 |
| Inbound | SSH | 22 | Bastion Host | 管理用SSH |
| Outbound | All | All | 0.0.0.0/0 | 全てのアウトバウンド |

#### Application Server (Private Subnet)

| Direction | Protocol | Port | Source | 説明 |
|-----------|----------|------|--------|------|
| Inbound | HTTP | 8000 | Web Server | APIアクセス |
| Inbound | SSH | 22 | Bastion Host | 管理用SSH |
| Outbound | All | All | 0.0.0.0/0 | 全てのアウトバウンド |

#### Database (Data Subnet)

| Direction | Protocol | Port | Source | 説明 |
|-----------|----------|------|--------|------|
| Inbound | PostgreSQL | 5432 | App Server | DB接続 |
| Inbound | SSH | 22 | Bastion Host | 管理用SSH |
| Outbound | PostgreSQL | 5432 | Read Replica | レプリケーション |

---

## コンピューティングリソース

### サーバースペック

#### Web Server

| 項目 | Development | Staging | Production |
|-----|------------|---------|-----------|
| インスタンスタイプ | t3.micro | t3.small | t3.medium |
| CPU | 1 vCPU | 2 vCPU | 2 vCPU |
| メモリ | 1GB | 2GB | 4GB |
| ストレージ | 8GB | 20GB | 30GB |
| 数量 | 1 | 2 | 4+ (Auto-scaling) |

#### Application Server

| 項目 | Development | Staging | Production |
|-----|------------|---------|-----------|
| インスタンスタイプ | t3.small | t3.medium | t3.large |
| CPU | 2 vCPU | 2 vCPU | 2 vCPU |
| メモリ | 2GB | 4GB | 8GB |
| ストレージ | 20GB | 30GB | 50GB |
| 数量 | 1 | 2 | 4+ (Auto-scaling) |

### Auto-scaling 設定

#### Web Server Auto-scaling

| 項目 | 設定値 |
|-----|-------|
| 最小インスタンス数 | 2 |
| 最大インスタンス数 | 10 |
| スケールアウト条件 | CPU使用率 > 70% for 5分 |
| スケールイン条件 | CPU使用率 < 30% for 10分 |
| クールダウン期間 | 5分 |

#### Application Server Auto-scaling

| 項目 | 設定値 |
|-----|-------|
| 最小インスタンス数 | 2 |
| 最大インスタンス数 | 20 |
| スケールアウト条件 | CPU使用率 > 70% または リクエスト数 > 1000/分 |
| スケールイン条件 | CPU使用率 < 30% かつ リクエスト数 < 300/分 |
| クールダウン期間 | 3分 |

---

## データベース構成

### PostgreSQL 設定

#### プライマリデータベース

| 項目 | Development | Staging | Production |
|-----|------------|---------|-----------|
| インスタンスタイプ | db.t3.micro | db.t3.small | db.r5.large |
| CPU | 1 vCPU | 2 vCPU | 2 vCPU |
| メモリ | 1GB | 2GB | 16GB |
| ストレージ | 20GB (GP2) | 50GB (GP3) | 500GB (GP3) |
| IOPS | - | 3,000 | 10,000 |
| Multi-AZ | No | No | Yes |
| バックアップ保持期間 | 1日 | 7日 | 30日 |

#### リードレプリカ

| 項目 | Staging | Production |
|-----|---------|-----------|
| 数量 | 1 | 2 |
| 配置 | 同一AZ | 異なるAZ |
| レプリケーション遅延 | < 1秒 | < 1秒 |

### キャッシュ (Redis)

| 項目 | Development | Staging | Production |
|-----|------------|---------|-----------|
| インスタンスタイプ | cache.t3.micro | cache.t3.small | cache.r5.large |
| メモリ | 0.5GB | 1.5GB | 13GB |
| レプリケーション | No | No | Yes (2 replicas) |
| クラスター | No | No | Yes |
| 自動フェイルオーバー | No | No | Yes |

---

## ストレージ

### オブジェクトストレージ (S3 / GCS / Azure Blob)

| バケット/コンテナ | 用途 | アクセス権限 | 暗号化 | バージョニング |
|------------------|------|------------|--------|--------------|
| `app-static` | 静的ファイル | Public Read | Yes | No |
| `app-uploads` | ユーザーアップロード | Private | Yes | Yes |
| `app-backups` | バックアップ | Private | Yes | Yes |
| `app-logs` | ログファイル | Private | Yes | No |

### ライフサイクルポリシー

| バケット | ルール | 期間 | アクション |
|---------|-------|------|----------|
| `app-uploads` | 古いファイル | 90日後 | Standard → Glacier |
| `app-uploads` | 削除マーカー | 365日後 | 完全削除 |
| `app-backups` | 古いバックアップ | 90日後 | Glacier Deep Archive |
| `app-logs` | 古いログ | 30日後 | 削除 |

---

## CDN / コンテンツ配信

### CDN 設定

| 項目 | 設定値 |
|-----|-------|
| プロバイダー | [CloudFront / Cloudflare / Fastly] |
| オリジンサーバー | [Load Balancer / S3] |
| キャッシュ動作 | 静的ファイル: 1年, API: キャッシュなし |
| 圧縮 | Gzip, Brotli有効 |
| HTTP/2 | 有効 |
| IPv6 | 有効 |
| SSL/TLS | TLS 1.2以上 |

### キャッシュ戦略

| パス | キャッシュTTL | キャッシュキー |
|-----|------------|-------------|
| `/static/*` | 1年 | URL |
| `/assets/*` | 1年 | URL |
| `/api/*` | なし | - |
| `/` | 1時間 | URL + Cookie |

---

## ロードバランシング

### ロードバランサー設定

| 項目 | 設定値 |
|-----|-------|
| タイプ | Application Load Balancer (Layer 7) |
| スキーム | Internet-facing |
| リスナー | HTTP (80), HTTPS (443) |
| ターゲットグループ | Web Servers, API Servers |
| ヘルスチェック | HTTP GET /health (30秒間隔) |
| セッション維持 | Cookie-based (1時間) |

### ルーティングルール

| 優先度 | パスパターン | ターゲット |
|-------|------------|----------|
| 1 | `/api/*` | API Server群 |
| 2 | `/static/*` | CDN (リダイレクト) |
| 3 | `/*` | Web Server群 |

---

## セキュリティ

### SSL/TLS 証明書

| 項目 | 設定値 |
|-----|-------|
| プロバイダー | Let's Encrypt / ACM |
| 証明書タイプ | ワイルドカード (`*.example.com`) |
| TLSバージョン | TLS 1.2, 1.3 |
| 暗号スイート | 強力な暗号スイートのみ |
| 自動更新 | 有効 |

### WAF (Web Application Firewall)

| ルール | アクション | 説明 |
|-------|----------|------|
| SQL Injection | Block | SQLインジェクション攻撃をブロック |
| XSS | Block | クロスサイトスクリプティングをブロック |
| Rate Limiting | Block | 1分間に100リクエスト超過でブロック |
| Geo-blocking | Block | 特定国からのアクセスをブロック（必要に応じて） |
| Known Bad IPs | Block | 既知の悪意あるIPをブロック |

### シークレット管理

| 項目 | ツール | 説明 |
|-----|-------|------|
| API Key | [Secrets Manager / Key Vault] | 外部APIキーの管理 |
| Database Password | [Secrets Manager / Key Vault] | DB接続情報の管理 |
| 暗号化キー | [KMS / Cloud KMS] | データ暗号化キーの管理 |
| SSL証明書 | [Certificate Manager / Key Vault] | SSL証明書の管理 |

---

## 監視・ログ

### 監視項目

#### インフラ監視

| 項目 | 閾値 | アラート条件 |
|-----|------|------------|
| CPU使用率 | 80% | 5分間継続 |
| メモリ使用率 | 85% | 5分間継続 |
| ディスク使用率 | 90% | 即座 |
| ネットワーク帯域 | 80% | 5分間継続 |
| ヘルスチェック失敗 | - | 2回連続失敗 |

#### アプリケーション監視

| 項目 | 閾値 | アラート条件 |
|-----|------|------------|
| レスポンスタイム | 2秒 | 平均値が5分間超過 |
| エラーレート | 1% | 5分間継続 |
| リクエスト数 | - | 急激な増減（50%以上） |
| データベース接続プール | 90% | 5分間継続 |

#### データベース監視

| 項目 | 閾値 | アラート条件 |
|-----|------|------------|
| CPU使用率 | 80% | 5分間継続 |
| 接続数 | 90% | 即座 |
| レプリケーション遅延 | 5秒 | 3分間継続 |
| ストレージ使用率 | 85% | 即座 |
| Slow Query | 5秒 | 発生時 |

### ログ管理

#### ログの種類

| ログタイプ | 保存期間 | 保存先 | 説明 |
|-----------|---------|--------|------|
| アクセスログ | 90日 | S3 / Cloud Storage | Webサーバー・ロードバランサーのアクセスログ |
| アプリケーションログ | 30日 | CloudWatch / Stackdriver | アプリケーションの動作ログ |
| エラーログ | 90日 | CloudWatch / Stackdriver | エラー・例外ログ |
| 監査ログ | 1年 | S3 / Cloud Storage | セキュリティ関連の操作ログ |
| データベースログ | 30日 | RDS Logs / Cloud SQL | クエリログ、スローログ |

#### ログ分析

| ツール | 用途 |
|-------|------|
| [Elasticsearch / CloudWatch Insights] | ログ検索・分析 |
| [Kibana / Grafana] | ログ可視化 |
| [Fluentd / Logstash] | ログ収集・転送 |

---

## バックアップ・災害復旧

### バックアップ戦略

#### データベースバックアップ

| 項目 | 設定値 |
|-----|-------|
| フルバックアップ | 日次（深夜2時） |
| 差分バックアップ | 6時間ごと |
| トランザクションログ | 連続（PITR対応） |
| 保持期間 | 30日 |
| バックアップ先 | S3 / GCS (Multi-region) |
| 暗号化 | AES-256 |
| 自動テスト | 週次でリストアテスト |

#### ファイルバックアップ

| 項目 | 設定値 |
|-----|-------|
| バックアップ頻度 | 日次 |
| 保持期間 | 90日 |
| バージョニング | 有効 |
| 暗号化 | 有効 |

### 災害復旧 (DR)

#### RPO / RTO 目標

| 項目 | 目標値 |
|-----|-------|
| RPO (Recovery Point Objective) | 1時間 |
| RTO (Recovery Time Objective) | 4時間 |

#### DR 戦略

| レベル | 戦略 | RTO | RPO | コスト |
|-------|------|-----|-----|------|
| Level 1 | バックアップ＆リストア | 24時間 | 24時間 | 低 |
| Level 2 | パイロットライト | 4-6時間 | 1-4時間 | 中 |
| Level 3 | ウォームスタンバイ | 1-2時間 | 数分 | 高 |
| Level 4 | ホットスタンバイ | 数分 | ほぼ0 | 最高 |

**推奨**: Level 2 (パイロットライト) を採用

#### DR 手順

1. **障害検知**: 監視システムが障害を検知
2. **影響評価**: 障害の範囲と影響を評価
3. **DR起動判断**: DR発動の判断
4. **リソース起動**: DRサイトのリソースを起動
5. **データリストア**: 最新のバックアップからデータをリストア
6. **動作確認**: システムの動作を確認
7. **DNSカットオーバー**: DNSをDRサイトに切り替え
8. **サービス復旧**: サービスを再開

---

## デプロイメント

### デプロイ戦略

#### Blue-Green Deployment

```
[Current: Blue Environment] ← 100% トラフィック
         ↓
[Deploy: Green Environment] ← 0% トラフィック
         ↓
[Test: Green Environment]
         ↓
[Switch: Green Environment] ← 100% トラフィック
         ↓
[Rollback Ready: Blue Environment] ← 0% トラフィック (24時間保持)
```

#### Canary Deployment

```
[Current: V1] ← 95% トラフィック
      ↓
[Deploy: V2] ← 5% トラフィック
      ↓
[Monitor & Validate]
      ↓
[Gradual Increase: V2] ← 10% → 25% → 50% → 100%
```

### CI/CD パイプライン

```
[Git Push]
    ↓
[CI Pipeline]
├── コードチェックアウト
├── 依存関係インストール
├── Lint & Format チェック
├── 単体テスト実行
├── ビルド
└── イメージ作成 & プッシュ
    ↓
[CD Pipeline - Staging]
├── Staging環境にデプロイ
├── 統合テスト実行
├── E2Eテスト実行
└── 承認待ち
    ↓
[CD Pipeline - Production]
├── Production環境にデプロイ
├── スモークテスト
└── 監視確認
```

---

## コンテナ化 (Docker / Kubernetes)

### Docker 構成

#### Dockerfile 例 (Backend)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Kubernetes 構成 (オプション)

#### リソース定義

| リソース | Replicas | CPU Request | CPU Limit | Memory Request | Memory Limit |
|---------|----------|-------------|-----------|----------------|--------------|
| Frontend | 3 | 100m | 500m | 128Mi | 512Mi |
| Backend | 5 | 200m | 1000m | 256Mi | 1Gi |
| Redis | 3 | 100m | 500m | 256Mi | 512Mi |

---

## コスト管理

### 月額コスト見積もり (Production環境)

| カテゴリー | サービス | 月額コスト (USD) |
|-----------|---------|----------------|
| コンピューティング | EC2 / GCE | $[500] |
| データベース | RDS / Cloud SQL | $[300] |
| ストレージ | S3 / GCS | $[100] |
| ネットワーク | データ転送 | $[200] |
| CDN | CloudFront / Cloudflare | $[150] |
| 監視 | CloudWatch / Stackdriver | $[50] |
| **合計** | | **$[1,300]** |

### コスト最適化戦略

1. **リザーブドインスタンス**: 1-3年契約で最大70%削減
2. **スポットインスタンス**: 非本番環境やバッチ処理に活用
3. **Auto-scaling**: 需要に応じた自動スケーリング
4. **ストレージライフサイクル**: 古いデータを安価なストレージに移動
5. **CDN活用**: オリジンへのトラフィックを削減

---

## 運用・保守

### メンテナンスウィンドウ

| 環境 | メンテナンスウィンドウ | 頻度 |
|-----|---------------------|------|
| Development | 随時 | - |
| Staging | 火曜日 2:00-4:00 JST | 週次 |
| Production | 第2・4火曜日 2:00-4:00 JST | 月2回 |

### パッチ適用ポリシー

| パッチタイプ | 適用タイミング | テスト要件 |
|------------|-------------|----------|
| セキュリティパッチ | 緊急時即座、通常時7日以内 | Staging環境で24時間動作確認 |
| 機能更新 | 月次メンテナンス | Staging環境で1週間動作確認 |
| マイナー更新 | 四半期ごと | Staging環境で2週間動作確認 |
| メジャー更新 | 年次 | Staging環境で1ヶ月動作確認 |

---

## アーキテクチャ更新履歴

| 日付 | 変更内容 | 理由 | 担当者 |
|-----|---------|------|--------|
| [YYYY-MM-DD] | [変更内容] | [理由] | [担当者] |
