from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path

from x_sleep_ops.config import load_config
from x_sleep_ops.daily_brief import load_or_generate_daily_brief, save_daily_brief
from x_sleep_ops.draft_service import build_draft_bundle
from x_sleep_ops.output_writer import append_review_logs, save_draft_markdown


def parse_date(date_str: str | None) -> date:
    if not date_str:
        return date.today()
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def cmd_daily(repo_root: Path, target_date: date, print_out: bool) -> int:
    config = load_config(repo_root)
    brand = config.get("brand", {})
    brief = load_or_generate_daily_brief(repo_root, target_date, brand)
    save_daily_brief(repo_root, target_date, brief)
    if print_out:
        print(brief)
    return 0


def cmd_draft(repo_root: Path, target_date: date) -> int:
    from x_sleep_ops.openai_client import OpenAIClientError, OpenAIResponsesClient

    config = load_config(repo_root)
    brand = config.get("brand", {})
    daily_brief = load_or_generate_daily_brief(repo_root, target_date, brand)

    try:
        client = OpenAIResponsesClient()
        bundle = build_draft_bundle(client, target_date, daily_brief, brand)
    except OpenAIClientError as exc:
        print(f"[error] {exc}")
        return 2

    md_path = save_draft_markdown(repo_root, bundle)
    csv_path = append_review_logs(repo_root, bundle)

    print(f"draft markdown: {md_path}")
    print(f"review log: {csv_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="x-sleep-ops automation")
    sub = parser.add_subparsers(dest="command", required=True)

    daily_parser = sub.add_parser("daily", help="daily brief を生成")
    daily_parser.add_argument("--date", default=None, help="YYYY-MM-DD")
    daily_parser.add_argument("--print", action="store_true", dest="print_out", help="標準出力に表示")

    draft_parser = sub.add_parser("draft", help="daily briefから投稿案生成〜レビューまで実行")
    draft_parser.add_argument("--date", default=None, help="YYYY-MM-DD")

    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parent

    if args.command == "daily":
        return cmd_daily(repo_root, parse_date(args.date), args.print_out)
    if args.command == "draft":
        return cmd_draft(repo_root, parse_date(args.date))

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
