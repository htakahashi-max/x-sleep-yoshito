from __future__ import annotations

import csv
from pathlib import Path

from x_sleep_ops.models import DraftBundle


def save_draft_markdown(repo_root: Path, bundle: DraftBundle) -> Path:
    out_path = repo_root / "output" / "drafts" / f"draft_{bundle.target_date.strftime('%Y%m%d')}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    lines.append(f"# Draft ({bundle.target_date.isoformat()})")
    lines.append("")
    lines.append("## 1. 今日の最優先テーマ")
    lines.append(bundle.priority_theme)
    lines.append("")
    lines.append("## 2-6. 投稿案・タイプ・note導線判定・チェック結果・修正版")
    for d in bundle.drafts:
        lines.append("")
        lines.append(f"### 投稿案 {d.index}")
        lines.append("**投稿案**")
        lines.append(d.text)
        lines.append("")
        lines.append(f"- 投稿タイプ: {d.post_type}")
        lines.append(f"- note導線判定: {d.note_lead_judgement}")
        lines.append("- 投稿前チェック結果:")
        lines.append(f"  - chk_target_fit: {d.check.chk_target_fit}")
        lines.append(f"  - chk_one_message: {d.check.chk_one_message}")
        lines.append(f"  - chk_practicality: {d.check.chk_practicality}")
        lines.append(f"  - chk_no_blame: {d.check.chk_no_blame}")
        lines.append(f"  - chk_no_medical_overclaim: {d.check.chk_no_medical_overclaim}")
        lines.append(f"  - chk_hook_strength: {d.check.chk_hook_strength}")
        lines.append(f"  - chk_actionable_end: {d.check.chk_actionable_end}")
        lines.append(f"  - final_decision: {d.check.final_decision}")
        lines.append(f"  - review_comment: {d.check.review_comment}")
        lines.append("")
        lines.append("**修正版**")
        lines.append(d.revised_text)

    lines.append("")
    lines.append("## 7. 今日一番おすすめの投稿")
    lines.append(f"投稿案 {bundle.recommended_index}")
    lines.append("")
    lines.append("## 8. 投稿前の最終確認ポイント")
    for point in bundle.final_checkpoints:
        lines.append(f"- {point}")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


def append_review_logs(repo_root: Path, bundle: DraftBundle) -> Path:
    path = repo_root / "post_review_logs.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    header = [
        "date",
        "draft_index",
        "post_type",
        "note_lead_judgement",
        "chk_target_fit",
        "chk_one_message",
        "chk_practicality",
        "chk_no_blame",
        "chk_no_medical_overclaim",
        "chk_hook_strength",
        "chk_actionable_end",
        "final_decision",
    ]
    file_exists = path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)
        for d in bundle.drafts:
            writer.writerow(
                [
                    bundle.target_date.isoformat(),
                    d.index,
                    d.post_type,
                    d.note_lead_judgement,
                    d.check.chk_target_fit,
                    d.check.chk_one_message,
                    d.check.chk_practicality,
                    d.check.chk_no_blame,
                    d.check.chk_no_medical_overclaim,
                    d.check.chk_hook_strength,
                    d.check.chk_actionable_end,
                    d.check.final_decision,
                ]
            )
    return path
