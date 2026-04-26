from __future__ import annotations

from datetime import date
from typing import Protocol

from x_sleep_ops.models import DraftBundle, DraftCandidate, DraftCheckResult


class JsonGeneratorClient(Protocol):
    def generate_json(self, system_prompt: str, user_prompt: str) -> dict:
        ...


GEN_SYSTEM_PROMPT = """あなたはX投稿案作成アシスタントです。
必ずJSONのみを返してください。説明文は不要です。"""

REVIEW_SYSTEM_PROMPT = """あなたはSNS投稿前レビュー担当です。
必ずJSONのみを返してください。"""


def generate_candidates(
    client: JsonGeneratorClient,
    daily_brief: str,
    brand: dict,
) -> tuple[str, list[dict]]:
    user_prompt = f"""
以下を踏まえて、X投稿案を3本作成してください。

# daily brief
{daily_brief}

# brand
{brand}

制約:
- 140〜280字程度
- 読みやすい改行
- 1投稿1テーマ
- 忙しい働く人向け
- 現実に続けやすい
- 読者を責めない
- 医療断定・誇張を避ける
- 最後に小さな行動 or 気づき

JSON schema:
{{
  "priority_theme": "string",
  "drafts": [
    {{"text": "string", "post_type": "string", "note_lead_judgement": "つながる|弱い|不要"}},
    ...3件
  ]
}}
"""
    data = client.generate_json(GEN_SYSTEM_PROMPT, user_prompt)
    return data["priority_theme"], data["drafts"]


def review_and_revise(client: JsonGeneratorClient, draft_text: str, brand: dict) -> tuple[DraftCheckResult, str]:
    user_prompt = f"""
次の投稿案をレビューして、必要なら修正版を作成してください。

投稿案:
{draft_text}

brand:
{brand}

判定項目:
- chk_target_fit
- chk_one_message
- chk_practicality
- chk_no_blame
- chk_no_medical_overclaim
- chk_hook_strength
- chk_actionable_end

各項目は yes/fix/no。
final_decision は 投稿OK/軽微修正して投稿/投稿見送り。

JSON schema:
{{
  "check": {{
    "chk_target_fit": "yes|fix|no",
    "chk_one_message": "yes|fix|no",
    "chk_practicality": "yes|fix|no",
    "chk_no_blame": "yes|fix|no",
    "chk_no_medical_overclaim": "yes|fix|no",
    "chk_hook_strength": "yes|fix|no",
    "chk_actionable_end": "yes|fix|no",
    "final_decision": "投稿OK|軽微修正して投稿|投稿見送り",
    "review_comment": "string"
  }},
  "revised_text": "string"
}}
"""
    data = client.generate_json(REVIEW_SYSTEM_PROMPT, user_prompt)
    chk = data["check"]
    result = DraftCheckResult(
        chk_target_fit=chk["chk_target_fit"],
        chk_one_message=chk["chk_one_message"],
        chk_practicality=chk["chk_practicality"],
        chk_no_blame=chk["chk_no_blame"],
        chk_no_medical_overclaim=chk["chk_no_medical_overclaim"],
        chk_hook_strength=chk["chk_hook_strength"],
        chk_actionable_end=chk["chk_actionable_end"],
        final_decision=chk["final_decision"],
        review_comment=chk["review_comment"],
    )
    return result, data["revised_text"]


def build_draft_bundle(
    client: JsonGeneratorClient,
    target_date: date,
    daily_brief: str,
    brand: dict,
) -> DraftBundle:
    priority_theme, generated = generate_candidates(client, daily_brief, brand)
    drafts: list[DraftCandidate] = []
    for idx, item in enumerate(generated, start=1):
        check, revised_text = review_and_revise(client, item["text"], brand)
        drafts.append(
            DraftCandidate(
                index=idx,
                text=item["text"],
                post_type=item.get("post_type", "不明"),
                note_lead_judgement=item.get("note_lead_judgement", "不要"),
                check=check,
                revised_text=revised_text,
            )
        )

    recommended = min(
        drafts,
        key=lambda d: (0 if d.check.final_decision == "投稿OK" else 1, d.index),
    )

    checkpoints = [
        "誤字脱字を最終確認する",
        "不必要に不安を煽る表現がないか確認する",
        "投稿時間帯が読者に合っているか確認する",
    ]

    return DraftBundle(
        target_date=target_date,
        priority_theme=priority_theme,
        daily_brief=daily_brief,
        drafts=drafts,
        recommended_index=recommended.index,
        final_checkpoints=checkpoints,
    )
