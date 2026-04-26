from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Literal

CheckState = Literal["yes", "fix", "no"]
FinalDecision = Literal["投稿OK", "軽微修正して投稿", "投稿見送り"]


@dataclass
class DraftCheckResult:
    chk_target_fit: CheckState
    chk_one_message: CheckState
    chk_practicality: CheckState
    chk_no_blame: CheckState
    chk_no_medical_overclaim: CheckState
    chk_hook_strength: CheckState
    chk_actionable_end: CheckState
    final_decision: FinalDecision
    review_comment: str


@dataclass
class DraftCandidate:
    index: int
    text: str
    post_type: str
    note_lead_judgement: str
    check: DraftCheckResult
    revised_text: str


@dataclass
class DraftBundle:
    target_date: date
    priority_theme: str
    daily_brief: str
    drafts: list[DraftCandidate]
    recommended_index: int
    final_checkpoints: list[str]
