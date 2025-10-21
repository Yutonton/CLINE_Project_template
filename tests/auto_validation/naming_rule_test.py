#!/usr/bin/env python3
"""
命名規則をチェックするスクリプト
"""

import os
import re
import sys
from pathlib import Path

def check_python_files():
    """Pythonファイルの命名規則チェック"""
    issues = []
    
    for root, dirs, files in os.walk('F_App/backend'):
        for file in files:
            if file.endswith('.py'):
                # snake_case チェック
                if not re.match(r'^[a-z_][a-z0-9_]*\.py$', file) and file != '__init__.py':
                    issues.append(f"Python: {os.path.join(root, file)} - snake_caseでない")
    
    return issues

def check_typescript_files():
    """TypeScriptファイルの命名規則チェック"""
    issues = []
    
    for root, dirs, files in os.walk('F_App/frontend/src'):
        for file in files:
            if file.endswith('.tsx') or file.endswith('.ts'):
                # PascalCase（コンポーネント）またはcamelCase
                if not re.match(r'^[A-Z][a-zA-Z0-9]*\.(tsx|ts)$', file) and \
                   not re.match(r'^[a-z][a-zA-Z0-9]*\.(tsx|ts)$', file) and \
                   file not in ['index.tsx', 'index.ts']:
                    issues.append(f"TS: {os.path.join(root, file)} - 命名規則違反")
    
    return issues

def main():
    print("🔍 命名規則チェック開始...")
    
    all_issues = []
    all_issues.extend(check_python_files())
    all_issues.extend(check_typescript_files())
    
    if all_issues:
        print("\n❌ 命名規則違反:")
        for issue in all_issues:
            print(f"  - {issue}")
        return 1
    
    print("\n✅ 命名規則OK")
    return 0

if __name__ == '__main__':
    sys.exit(main())
