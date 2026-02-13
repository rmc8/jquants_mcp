# jquants-mcp

J-Quants API (日本の金融データAPI) を利用するための Model Context Protocol (MCP) サーバーです。
Claude Desktop などの MCP クライアントから、日本株の株価、財務情報、指数、信用残高などのデータを直接取得・分析できます。

**注意**: このツールは PyPI には公開されていません。Git リポジトリから直接利用することを想定しています。

## 機能 (Tools)

合計11個のツールを提供し、個人投資家による分析に必要な情報を網羅しています。

### 基本情報・株価
- **`get_listed_issues`**: 上場銘柄一覧（銘柄コード、業種など）
- **`get_daily_quotes`**: 日次株価データ（四本値、出来高、売買代金）
- **`get_indices_daily`**: 指数データ（TOPIX, 日経225など）

### 財務・決算
- **`get_financial_summary`**: 財務サマリー（売上高、営業利益、EPSなど）
- **`get_financial_statements_detail`**: 財務諸表詳細（BS/PL/CFの全項目）
- **`get_financial_dividends`**: 配当金情報（配当落日、確定日、配当金額）
- **`get_earnings_calendar`**: 決算発表予定日

### 市場分析・需給 (異常値検知)
- **`get_market_segment_breakdown`**: 売買内訳データ
- **`get_short_sale_ratio`**: 空売り比率情報
- **`get_market_margin_interest`**: 信用取引週末残高（貸借倍率、回転日数など）
- **`get_investor_trading_trends`**: 投資部門別売買状況（外国人・個人などの売買動向）

## 前提条件

1. **J-Quants API プラン**: J-Quants API の利用契約（FreeプランまたはPremiumプラン）が必要です。
2. **API Key (Refresh Token)**: J-Quants のマイページからリフレッシュトークンを取得してください。
3. **uv**: Python パッケージマネージャー [uv](https://github.com/astral-sh/uv) のインストールが必要です。

## インストールと設定

`uv` を使用して、Gitリポジトリからインストールするか、直接実行します。

### 方法1: `uv tool` としてインストール (推奨)

ツールとしてインストールすると、PATHにコマンドが追加され、どこからでも実行できるようになります。

```bash
# Gitリポジトリから直接インストール
uv tool install git+https://github.com/your-username/jquants-mcp.git

# または、ローカルディレクトリからインストール
uv tool install .
```

**Claude Desktop 設定 (`claude_desktop_config.json`)**:

```json
{
  "mcpServers": {
    "jquants": {
      "command": "jquants-mcp",
      "env": {
        "JQUANTS_API_KEY": "あなたのリフレッシュトークンをここに貼り付け"
      }
    }
  }
}
```

### 方法2: `uv run` で実行 (開発用)

リポジトリをクローンして、その場でのみ実行する場合です。

`claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "jquants": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/jquants-mcp",
        "run",
        "jquants-mcp"
      ],
      "env": {
        "JQUANTS_API_KEY": "あなたのリフレッシュトークンをここに貼り付け"
      }
    }
  }
}
```
※ `/path/to/jquants-mcp` は実際のパスに置き換えてください。

## 開発者向け情報

- **構成**:
  - `jquants_mcp/__main__.py`: エントリーポイント、MCPツールの定義
  - `jquants_mcp/libs/client.py`: J-Quants API クライアントの初期化
  - `jquants_mcp/libs/models.py`: Pydantic データモデル (入力バリデーション)

- **依存ライブラリ**:
  - `jquants-api-client`: 公式APIクライアント (v2.0.0以上)
  - `mcp`: MCP SDK
  - `pydantic`: バリデーション
  - `pandas`: データ処理 (`jquants-api-client` の依存)

## ライセンス

MIT License
