from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any
from urllib import error, request


class OpenAIClientError(RuntimeError):
    pass


@dataclass
class OpenAIResponsesClient:
    model: str = "gpt-4.1-mini"
    timeout_seconds: int = 90

    def __post_init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise OpenAIClientError(
                "OPENAI_API_KEY が未設定です。環境変数にAPIキーを設定してください。"
            )

    def generate_json(self, system_prompt: str, user_prompt: str) -> dict[str, Any]:
        payload = {
            "model": self.model,
            "input": [
                {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
                {"role": "user", "content": [{"type": "text", "text": user_prompt}]},
            ],
        }
        req = request.Request(
            "https://api.openai.com/v1/responses",
            method="POST",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            data=json.dumps(payload).encode("utf-8"),
        )
        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as resp:
                raw = resp.read().decode("utf-8")
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="ignore")
            raise OpenAIClientError(f"OpenAI API error: {exc.code} {body}") from exc
        except error.URLError as exc:
            raise OpenAIClientError(f"OpenAI API connection error: {exc}") from exc

        parsed = json.loads(raw)
        output_text = self._extract_text(parsed)
        try:
            return json.loads(output_text)
        except json.JSONDecodeError as exc:
            raise OpenAIClientError(f"JSON parse error: {exc}\nRaw output: {output_text}") from exc

    @staticmethod
    def _extract_text(payload: dict[str, Any]) -> str:
        for item in payload.get("output", []):
            if item.get("type") != "message":
                continue
            for part in item.get("content", []):
                if part.get("type") in {"output_text", "text"}:
                    text = part.get("text", "")
                    if text:
                        return text
        raise OpenAIClientError(f"No output text in payload: {payload}")
