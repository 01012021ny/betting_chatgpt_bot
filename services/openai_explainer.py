from __future__ import annotations

from openai import AsyncOpenAI


class OpenAIExplainer:
    def __init__(self, api_key: str, model: str) -> None:
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def enrich_explanation(self, short_reason: str) -> str:
        # Optional enhancement path. Core bot works with rule-based explanations even without OpenAI.
        completion = await self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": "Ты аналитик ставок. Дай краткое нейтральное объяснение до 25 слов без обещаний выигрыша.",
                },
                {"role": "user", "content": short_reason},
            ],
            max_output_tokens=80,
        )
        return completion.output_text.strip()
