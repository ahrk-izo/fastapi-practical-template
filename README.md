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
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_main.py
├── .dockerignore
├── .gitignore
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

### テストの実行

```bash
uv run pytest
```

### Lintの実行

```bash
uv run ruff check .
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
{"status":"ok"}
```

## Dockerでの起動

Dockerを使ってAPIサーバーを起動します。

```bash
docker compose up --build
```

ヘルスチェック：

```bash
curl http://127.0.0.1:8000/health
```

期待するレスポンス：

```json
{"status":"ok"}
```

停止する場合：

```bash
docker compose down
```


## このリポジトリで意識していること

このリポジトリでは、コードだけでなく、実務での開発を想定した構成や運用も重視しています。
具体的には、以下のような点を意識しています。
- ローカル環境に依存しすぎない開発環境
- テストしやすい構成
- 小さな変更単位でのコミット
- Pull Requestを使った変更管理
- READMEによる利用手順の明文化

