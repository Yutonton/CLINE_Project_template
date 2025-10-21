#!/usr/bin/env python3
"""
ドキュメント間の整合性をチェックするスクリプト
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath: str) -> bool:
    """ファイルの存在確認"""
    return Path(filepath).exists()

def check_required_files():
    """必須ファイルの存在確認"""
    required_files = [
        'README.md',
        'A_Requirements/overview.md',
        'A_Requirements/functional_nonfunctional.md',
        'A_Requirements/user_stories.md',
        'B_Architecture/tech_stack.md',
        'B_Architecture/repo_structure.md',
        'B_Architecture/infra_architecture.md',
        'C_DataModel/entity_relation.md',
        'C_DataModel/db_schema.md',
        'D_API/endpoints.md',
        'D_API/data_flow.md',
        'D_API/api_authentication.md',
        'E_UI/screen_list.md',
        'E_UI/component_spec.md',
        'E_UI/design_guideline_ref.md',
        'rules/coding_standard.md',
        'rules/security_policy.md',
    ]
    
    missing_files = []
    for file in required_files:
        if not check_file_exists(file):
            missing_files.append(file)
    
    return missing_files

def main():
    print("🔍 ドキュメント整合性チェック開始...")
    
    # 必須ファイルチェック
    missing = check_required_files()
    if missing:
        print("\n❌ 以下のファイルが見つかりません:")
        for file in missing:
            print(f"  - {file}")
        return 1
    
    print("\n✅ すべての必須ファイルが存在します")
    return 0

if __name__ == '__main__':
    sys.exit(main())
