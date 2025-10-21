# デザインガイドライン参照

UIデザインの統一基準を定義します。

## 概要

このドキュメントでは、カラーパレット、タイポグラフィ、スペーシング、アイコンなど、デザインシステムの基礎を明確にします。

---

## カラーパレット

### プライマリーカラー

| 用途 | カラー | Hex | 使用例 |
|-----|-------|-----|--------|
| Primary | 青 | `#0066CC` | メインボタン、リンク |
| Primary Hover | 濃青 | `#0052A3` | ホバー状態 |
| Primary Light | 薄青 | `#E6F2FF` | 背景 |

### セカンダリーカラー

| 用途 | カラー | Hex |
|-----|-------|-----|
| Secondary | グレー | `#6B7280` |
| Success | 緑 | `#10B981` |
| Warning | 黄 | `#F59E0B` |
| Danger | 赤 | `#EF4444` |
| Info | 水色 | `#3B82F6` |

### ニュートラルカラー

| 用途 | Hex | 使用例 |
|-----|-----|--------|
| Black | `#000000` | テキスト |
| Gray 900 | `#111827` | 見出し |
| Gray 700 | `#374151` | 本文 |
| Gray 500 | `#6B7280` | 補助テキスト |
| Gray 300 | `#D1D5DB` | ボーダー |
| Gray 100 | `#F3F4F6` | 背景 |
| White | `#FFFFFF` | 背景 |

---

## タイポグラフィ

### フォントファミリー

```css
--font-family-base: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
--font-family-mono: 'Courier New', Courier, monospace;
```

### フォントサイズ

| サイズ | px | rem | 用途 |
|-------|----|----|------|
| xs | 12px | 0.75rem | キャプション |
| sm | 14px | 0.875rem | 補助テキスト |
| base | 16px | 1rem | 本文 |
| lg | 18px | 1.125rem | リード文 |
| xl | 20px | 1.25rem | 小見出し |
| 2xl | 24px | 1.5rem | 見出し3 |
| 3xl | 30px | 1.875rem | 見出し2 |
| 4xl | 36px | 2.25rem | 見出し1 |

### フォントウェイト

| ウェイト | 値 | 用途 |
|---------|---|------|
| Light | 300 | - |
| Regular | 400 | 本文 |
| Medium | 500 | 強調 |
| Semibold | 600 | 小見出し |
| Bold | 700 | 見出し |

### 行間

| サイズ | 行間 |
|-------|------|
| Tight | 1.25 |
| Normal | 1.5 |
| Relaxed | 1.75 |
| Loose | 2.0 |

---

## スペーシング

### 8pxグリッドシステム

| サイズ | px | rem | 用途 |
|-------|----|----|------|
| 0 | 0px | 0 | - |
| 1 | 4px | 0.25rem | 最小間隔 |
| 2 | 8px | 0.5rem | 小間隔 |
| 3 | 12px | 0.75rem | - |
| 4 | 16px | 1rem | 標準 |
| 6 | 24px | 1.5rem | 中間隔 |
| 8 | 32px | 2rem | 大間隔 |
| 12 | 48px | 3rem | セクション間 |
| 16 | 64px | 4rem | 大セクション |

---

## ブレークポイント

```css
/* Mobile First */
--breakpoint-sm: 640px;   /* Small devices */
--breakpoint-md: 768px;   /* Tablets */
--breakpoint-lg: 1024px;  /* Desktops */
--breakpoint-xl: 1280px;  /* Large desktops */
--breakpoint-2xl: 1536px; /* Extra large */
```

---

## ボーダー

### ボーダー半径

| サイズ | px | 用途 |
|-------|----|----|
| None | 0px | - |
| sm | 4px | 小要素 |
| base | 6px | ボタン、カード |
| lg | 8px | 大要素 |
| full | 9999px | 円形 |

### ボーダー幅

| サイズ | px |
|-------|-----|
| 0 | 0px |
| 1 | 1px |
| 2 | 2px |
| 4 | 4px |

---

## シャドウ

```css
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-base: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
```

---

## アイコン

### アイコンライブラリ

推奨: **Heroicons**, **Feather Icons**, **Material Icons**

### アイコンサイズ

| サイズ | px | 用途 |
|-------|----|----|
| xs | 16px | インラインアイコン |
| sm | 20px | ボタン内アイコン |
| base | 24px | 標準 |
| lg | 32px | 大アイコン |
| xl | 48px | ヒーローアイコン |

---

## アニメーション

### トランジション

```css
--transition-fast: 150ms ease-in-out;
--transition-base: 300ms ease-in-out;
--transition-slow: 500ms ease-in-out;
```

### イージング

```css
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
```

---

## Zインデックス

| レイヤー | z-index | 用途 |
|---------|---------|------|
| Base | 0 | 通常要素 |
| Dropdown | 1000 | ドロップダウン |
| Sticky | 1020 | 固定ヘッダー |
| Modal Backdrop | 1040 | モーダル背景 |
| Modal | 1050 | モーダル |
| Popover | 1060 | ポップオーバー |
| Tooltip | 1070 | ツールチップ |
| Toast | 1080 | 通知 |

---

## 参考デザインシステム

プロジェクトのデザインガイドラインは以下を参考にしています：

- **Material Design**: https://material.io/design
- **Tailwind CSS**: https://tailwindcss.com/docs
- **Ant Design**: https://ant.design/
- **Chakra UI**: https://chakra-ui.com/

---

## デザインツール

### Figma

- デザインファイル: [Figmaリンク]
- プロトタイプ: [Figmaリンク]

### スタイルガイド

- Storybook: [URL]

---

## 更新履歴

| 日付 | 変更内容 | 担当者 |
|-----|---------|--------|
| [YYYY-MM-DD] | [変更内容] | [担当者] |
