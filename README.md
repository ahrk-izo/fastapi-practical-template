# FastAPI Practical Template

FastAPIを使った、実務を意識したバックエンドAPIのテンプレートです。

このリポジトリでは、単にFastAPIを動かすだけでなく、Docker、テスト、Lint、CI/CDなど、実際の開発現場で必要になりやすい構成を段階的に整備していきます。

## 目的

このリポジトリの目的は、FastAPIを使った小規模なバックエンドAPI開発の基本構成を整理することです。

特に以下を意識しています。

- わかりやすいディレクトリ構成
- Dockerを使ったローカル開発環境
- pytestによる自動テスト
- RuffによるLint
- GitHub ActionsによるCI
- 環境変数を使った設定管理
- 実務で拡張しやすい構成
- APIルーターを分割し、エンドポイント定義を管理しやすい構成にする


## 技術スタック

- Python
- FastAPI
- Docker
- pytest
- Ruff
- GitHub Actions
- uv

## 現在の構成
```text
fastapi-practical-template/
├── app/
│   ├── routers/
│   │   ├── __init__.py
│   │   └── health.py
│   ├── __init__.py
│   ├── config.py
│   ├── error_handlers.py
│   ├── logging_config.py
│   └── main.py
├── tests/
│   ├── test_config.py
│   ├── test_error_handlers.py
│   ├── test_logging_config.py
│   └── test_main.py
├── .dockerignore
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── .python-version
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
└── README.md
```

## セットアップ

### 依存関係のインストール

```bash
uv sync
```

## テスト・Lint・フォーマット

### テストの実行

```bash
uv run pytest
```

### Lintチェック

```bash
uv run ruff check .
```

### Lintの自動修正

```bash
uv run ruff check . --fix
```

### コードフォーマット

```bash
uv run ruff format .
```

### PR作成前の確認

PR作成前は、以下を実行します。

```bash
uv run ruff check . --fix
uv run ruff format .
uv run ruff check .
uv run pytest
```


## アプリケーションの起動

### ローカルで起動する場合

```bash
uv run uvicorn app.main:app --reload
```

以下にアクセスします。

```text
http://127.0.0.1:8000/health
```

期待するレスポンス：

```json
{"status":"ok","environment":"local"}
```

## 環境変数を指定して起動する場合

環境変数を指定することで、アプリケーションの設定値を変更できます。

```bash
APP_ENV=development APP_DEBUG=true LOG_LEVEL=DEBUG uv run uvicorn app.main:app --reload
```

ヘルスチェック：

```bash
curl -s http://127.0.0.1:8000/health -w "\n"
```

期待するレスポンス：

```json
{"status":"ok","environment":"development"}
```


## Dockerでの起動

Dockerを使ってAPIサーバーを起動します。

```bash
docker compose up --build
```

ヘルスチェック：

```bash
curl -s http://127.0.0.1:8000/health -w "\n"
```

期待するレスポンス：

```json
{"status":"ok","environment":"development"}
```

停止する場合：

```bash
docker compose down
```

## 設定管理

アプリケーション設定は `app/config.py` に集約しています。

現在は以下の環境変数を使用できます。

| 環境変数 | 内容 | デフォルト値 |
|---|---|---|
| `APP_NAME` | アプリケーション名 | `FastAPI Practical Template` |
| `APP_VERSION` | アプリケーションバージョン | `0.1.0` |
| `APP_ENV` | 実行環境名 | `local` |
| `APP_DEBUG` | デバッグモード | `false` |
| `LOG_LEVEL` | ログレベル | `INFO` |

例：

```bash
APP_ENV=development APP_DEBUG=true LOG_LEVEL=DEBUG uv run uvicorn app.main:app --reload
```


## ロギング

アプリケーションのログ設定は `app/logging_config.py` に集約しています。

ログレベルは `LOG_LEVEL` 環境変数で変更できます。

例：

```bash
LOG_LEVEL=DEBUG uv run uvicorn app.main:app --reload
```

Docker起動時は `docker-compose.yml` で以下の環境変数を指定しています。

```yaml
environment:
  APP_NAME: FastAPI Practical Template
  APP_VERSION: 0.1.0
  APP_ENV: development
  APP_DEBUG: "true"
  LOG_LEVEL: DEBUG
```

これにより、Docker起動時は開発環境向けの設定でアプリケーションを起動できます。

## エラーハンドリング

共通エラーハンドリングは `app/error_handlers.py` に集約しています。

HTTPエラーや想定外エラーが発生した場合、以下のような共通形式でレスポンスを返します。

```json
{
  "error": {
    "type": "http_error",
    "message": "Not Found",
    "status_code": 404
  }
}
```

### HTTPエラーの確認

存在しないURLにアクセスすると、共通エラーレスポンス形式で404エラーを返します。

```bash
curl -s http://127.0.0.1:8000/not-found -w "\n"
```

期待するレスポンス：

```json
{"error":{"type":"http_error","message":"Not Found","status_code":404}}
```

想定外エラーの場合は、内部情報をレスポンスに含めず、以下の形式で返します。

```json
{
  "error": {
    "type": "internal_server_error",
    "message": "Internal server error",
    "status_code": 500
  }
}
```

想定外エラーの詳細はログに出力し、APIレスポンスには一般的なエラーメッセージのみを返します。


## CI

このリポジトリでは、GitHub Actionsを使ってPull Request作成時およびmainブランチへのpush時に、Lintとテストを自動実行します。

実行しているチェックは以下です。

```bash
uv run ruff check .
uv run pytest
```

これにより、コード変更時に最低限の品質確認を自動化しています。


## 開発フロー

このリポジトリでは、実務を意識して以下の流れで開発を進めています。

```text
Issue作成
↓
featureブランチ作成
↓
実装
↓
Pull Request作成
↓
CI確認
↓
mainブランチへマージ
```


## このリポジトリで意識していること

このリポジトリでは、コードだけでなく、実務での開発を想定した構成や運用も重視しています。
具体的には、以下のような点を意識しています。
- ローカル環境に依存しすぎない開発環境
- テストしやすい構成
- 小さな変更単位でのコミット
- Pull Requestを使った変更管理
- READMEによる利用手順の明文化

