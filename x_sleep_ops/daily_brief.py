from __future__ import annotations

from datetime import date
from pathlib import Path


def _daily_brief_path(repo_root: Path, target_date: date) -> Path:
    return repo_root / "output" / "daily_briefs" / f"daily_{target_date.strftime('%Y%m%d')}.md"


def build_daily_brief(target_date: date, brand: dict[str, str]) -> str:
    return (
        f"# Daily Brief ({target_date.isoformat()})\n\n"
        f"- 想定読者: {brand.get('audience', '忙しい働く人')}\n"
        f"- ブランドトーン: {brand.get('voice', '')}\n"
        f"- 禁止表現: {brand.get('banned_claims', '')}\n"
        "- 重点テーマ: 月曜は『睡眠の土台づくり』、火曜は『日中の眠気対策』、"
        "水曜は『夜のルーティン』、木曜は『ストレスと睡眠』、"
        "金曜は『週末リセット』、土日は『回復と振り返り』\n"
        "- 今日の依頼: X投稿3本。1投稿1テーマで、最後に小さな行動提案を入れる。\n"
    )


def load_or_generate_daily_brief(repo_root: Path, target_date: date, brand: dict[str, str]) -> str:
    path = _daily_brief_path(repo_root, target_date)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return path.read_text(encoding="utf-8")

    brief = build_daily_brief(target_date, brand)
    path.write_text(brief, encoding="utf-8")
    return brief


def save_daily_brief(repo_root: Path, target_date: date, content: str) -> Path:
    path = _daily_brief_path(repo_root, target_date)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path
