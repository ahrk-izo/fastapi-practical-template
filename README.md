# FastAPI Practical Template

FastAPIを使った、実務を意識したバックエンドAPIのテンプレートです。

単にFastAPIを起動するだけでなく、設定管理、ロギング、エラーハンドリング、Docker、テスト、Lint、CI、カバレッジ確認など、実際の開発現場で必要になりやすい構成を段階的に整備しています。

## このリポジトリについて

このリポジトリは、小規模なバックエンドAPIをFastAPIで開発する際の基本構成を整理することを目的としています。

サンプルAPIとして、DBを使わないインメモリのタスク管理APIを用意しています。
これにより、FastAPIのルーター分割、Pydanticスキーマ、共通エラーハンドリング、テストの書き方を確認できます。

## このリポジトリで示したいこと

このリポジトリでは、以下のような実務的な開発要素を示すことを意識しています。

* わかりやすいディレクトリ構成
* 環境変数を使った設定管理
* ロギング設定の分離
* APIルーターの分割
* Pydanticスキーマによるリクエスト/レスポンス定義
* 共通エラーハンドリング
* pytestによる自動テスト
* RuffによるLintとフォーマット
* pytest-covによるカバレッジ確認
* Dockerを使ったローカル開発環境
* GitHub ActionsによるCI
* Pull Requestを使った変更管理

## 主な機能

* ヘルスチェックAPI
* タスク管理APIサンプル

  * タスク一覧取得
  * タスク作成
  * タスク詳細取得
  * 存在しないタスクID指定時の404エラー
* 環境変数による設定管理
* ログレベル切り替え
* 共通エラーレスポンス
* テストカバレッジ確認
* CIでのLint、テスト、カバレッジ確認
* CIでのHTMLカバレッジレポート保存

## 技術スタック

* Python
* FastAPI
* Pydantic
* Docker
* pytest
* pytest-cov
* Ruff
* GitHub Actions
* uv

## ディレクトリ構成

```text
fastapi-practical-template/
├── app/
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   └── tasks.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── task.py
│   ├── __init__.py
│   ├── config.py
│   ├── error_handlers.py
│   ├── logging_config.py
│   └── main.py
├── tests/
│   ├── test_config.py
│   ├── test_error_handlers.py
│   ├── test_logging_config.py
│   ├── test_main.py
│   └── test_tasks.py
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

依存関係をインストールします。

```bash
uv sync
```

## アプリケーションの起動

### ローカルで起動する場合

```bash
uv run uvicorn app.main:app --reload
```

ヘルスチェック：

```bash
curl -s http://127.0.0.1:8000/health -w "\n"
```

期待するレスポンス：

```json
{"status":"ok","environment":"local"}
```

### 環境変数を指定して起動する場合

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

### Dockerで起動する場合

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

## APIサンプル

### ヘルスチェック

```bash
curl -s http://127.0.0.1:8000/health -w "\n"
```

期待するレスポンス：

```json
{"status":"ok","environment":"development"}
```

### タスク管理API

このリポジトリでは、FastAPIのルーター分割、Pydanticスキーマ、テスト、共通エラーハンドリングの実装例として、簡単なタスク管理APIを用意しています。

このAPIはサンプル実装のため、DBには保存せず、インメモリでタスクを管理します。

#### タスク一覧取得

```bash
curl -s http://127.0.0.1:8000/tasks -w "\n"
```

期待レスポンス：

```json
[]
```

#### タスク作成

```bash
curl -s -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"READMEを更新する","description":"タスク管理APIの説明を追加する"}' \
  -w "\n"
```

期待レスポンス：

```json
{"id":1,"title":"READMEを更新する","description":"タスク管理APIの説明を追加する","completed":false}
```

#### タスク詳細取得

```bash
curl -s http://127.0.0.1:8000/tasks/1 -w "\n"
```

期待レスポンス：

```json
{"id":1,"title":"READMEを更新する","description":"タスク管理APIの説明を追加する","completed":false}
```

#### 存在しないタスクIDを指定した場合

```bash
curl -s http://127.0.0.1:8000/tasks/999 -w "\n"
```

期待レスポンス：

```json
{"error":{"type":"http_error","message":"Task not found","status_code":404}}
```

## 設定管理

アプリケーション設定は `app/config.py` に集約しています。

現在は以下の環境変数を使用できます。

| 環境変数          | 内容            | デフォルト値                       |
| ------------- | ------------- | ---------------------------- |
| `APP_NAME`    | アプリケーション名     | `FastAPI Practical Template` |
| `APP_VERSION` | アプリケーションバージョン | `0.1.0`                      |
| `APP_ENV`     | 実行環境名         | `local`                      |
| `APP_DEBUG`   | デバッグモード       | `false`                      |
| `LOG_LEVEL`   | ログレベル         | `INFO`                       |

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

## テスト・Lint・カバレッジ

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

### テストカバレッジの確認

pytest-cov を使って、テストカバレッジを確認します。

```bash
uv run pytest --cov=app --cov-report=term-missing --cov-fail-under=80
```

`term-missing` を指定すると、テストされていない行を確認できます。

HTML形式で確認する場合は、以下を実行します。

```bash
uv run pytest --cov=app --cov-report=html
```

実行後、`htmlcov/index.html` をブラウザで開きます。

```bash
open htmlcov/index.html
```

### PR作成前の確認

PR作成前は、以下を実行します。

```bash
uv run ruff check . --fix
uv run ruff format .
uv run ruff check .
uv run pytest
uv run pytest --cov=app --cov-report=term-missing --cov-report=html --cov-fail-under=80
```

## CI

このリポジトリでは、GitHub Actionsを使ってPull Request作成時およびmainブランチへのpush時に、Lint、テスト、カバレッジ確認を自動実行します。

実行しているチェックは以下です。

```bash
uv run ruff check .
uv run pytest --cov=app --cov-report=term-missing --cov-report=html --cov-fail-under=80
```

CIでは、HTMLカバレッジレポートを `coverage-html` というartifactとして保存します。

これにより、コード変更時にLint、テスト、カバレッジを確認できるようにしています。

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
自己レビューコメント
↓
mainブランチへマージ
```

Pull Requestでは、1人開発でも確認内容を明記し、必要に応じて「自己レビュー済み」のコメントを残します。

## 今後の拡張予定

今後は、必要に応じて以下のような拡張を検討します。

* タスク更新APIの追加
* タスク削除APIの追加
* DB永続化
* SQLAlchemyの導入
* マイグレーション管理
* Repository層の追加
* 認証・認可の追加
* バリデーションエラーのレスポンス整理

## 備考

このリポジトリは、学習用のサンプルにとどまらず、実務での開発フローや品質確認を意識した構成を整理するためのポートフォリオです。
