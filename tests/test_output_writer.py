from __future__ import annotations

from datetime import date
from pathlib import Path

from x_sleep_ops.models import DraftBundle, DraftCandidate, DraftCheckResult
from x_sleep_ops.output_writer import append_review_logs, save_draft_markdown


def sample_bundle() -> DraftBundle:
    chk = DraftCheckResult(
        chk_target_fit="yes",
        chk_one_message="yes",
        chk_practicality="fix",
        chk_no_blame="yes",
        chk_no_medical_overclaim="yes",
        chk_hook_strength="fix",
        chk_actionable_end="yes",
        final_decision="軽微修正して投稿",
        review_comment="導入を短くするとより良い",
    )
    draft = DraftCandidate(
        index=1,
        text="sample",
        post_type="tips",
        note_lead_judgement="つながる",
        check=chk,
        revised_text="revised",
    )
    return DraftBundle(
        target_date=date(2026, 4, 26),
        priority_theme="夜のルーティン",
        daily_brief="brief",
        drafts=[draft],
        recommended_index=1,
        final_checkpoints=["A", "B"],
    )


def test_markdown_and_csv(tmp_path: Path) -> None:
    bundle = sample_bundle()
    md = save_draft_markdown(tmp_path, bundle)
    csv_path = append_review_logs(tmp_path, bundle)

    assert md.exists()
    assert csv_path.exists()
    assert "今日の最優先テーマ" in md.read_text(encoding="utf-8")
    csv_text = csv_path.read_text(encoding="utf-8")
    assert "chk_target_fit" in csv_text
