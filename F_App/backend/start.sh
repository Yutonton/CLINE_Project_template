#!/bin/bash
# Renderデプロイ用起動スクリプト
# リポジトリルートから実行されるため、F_App/backend に cd してから uvicorn を起動する
cd "$(dirname "$0")"
exec uvicorn src.main:app --host 0.0.0.0 --port "${PORT:-8000}"
