# x-sleep-yoshito

daily brief 生成〜X投稿案の作成・投稿前チェック・修正版保存を自動化するMVPです。

## セットアップ

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest
```

OpenAI APIキーを環境変数に設定します（**コードに直書きしない**）。

```bash
export OPENAI_API_KEY="<your-api-key>"
```

## 使い方

### 1) daily briefのみ生成

```bash
python3 main.py daily --print
# または
python3 main.py daily --date 2026-04-26 --print
```

- 既に `output/daily_briefs/daily_YYYYMMDD.md` があれば再利用します。
- なければ自動生成して保存します。

### 2) draft生成（今回追加）

```bash
python3 main.py draft
# または
python3 main.py draft --date 2026-04-26
```

実行時に以下を自動で行います。

1. daily brief の生成または読み込み
2. OpenAI Responses APIでX投稿案3本を生成
3. 各投稿案の投稿前チェック
4. 必要に応じて修正版を生成
5. Markdown保存
6. `post_review_logs.csv` へのチェック結果追記

出力先:

- `output/drafts/draft_YYYYMMDD.md`
- `post_review_logs.csv`

## 実装構成

- `main.py`: CLIエントリポイント（`daily` / `draft`）
- `x_sleep_ops/openai_client.py`: OpenAI Responses API クライアント
- `x_sleep_ops/draft_service.py`: 生成ロジック・レビュー/修正ロジック
- `x_sleep_ops/output_writer.py`: Markdown出力・CSV追記
- `x_sleep_ops/daily_brief.py`: daily brief の生成/読込
- `x_sleep_ops/models.py`: データモデル

## テスト

```bash
pytest -q
```
