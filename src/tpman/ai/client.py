"""OpenAI-compatible client wrapper."""

from typing import Any

from openai import OpenAI

from tpman.config import settings


class AIClient:
    """Lightweight wrapper for OpenAI-compatible APIs."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
    ) -> None:
        self.client = OpenAI(
            api_key=api_key or settings.openai_api_key,
            base_url=base_url or settings.openai_base_url,
        )
        self.model = model or settings.openai_model

    def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        """Send a chat completion request.

        Args:
            messages: List of message dicts with 'role' and 'content'.
            **kwargs: Additional parameters.

        Returns:
            Assistant response text.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,  # type: ignore[arg-type]
            **kwargs,
        )
        return response.choices[0].message.content or ""
