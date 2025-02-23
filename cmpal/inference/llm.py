from ollama import Client

from cmpal.inference.prompts import (
    GIT_COMMIT_MESSAGE_SYSTEM_PROMPT,
    GIT_COMMIT_MESSAGE_USER_PROMPT,
)
from cmpal.models.config import CommitStyleConfigs


class OllamaEngine:
    def __init__(
        self,
        config: CommitStyleConfigs,
        host: str = "http://localhost:11434",
        model: str = "qwen2.5-coder:7b",
        headers=None,
    ):
        self._client = Client(host=host, headers=headers or {"x-some-header": "some-value"})
        self._model = model
        self._config = config

    def _create_messages(self, diff: str):
        return [
            {
                "role": "system",
                "content": GIT_COMMIT_MESSAGE_SYSTEM_PROMPT.format(
                    style_config=self._config.pretty_print()
                ),
            },
            {
                "role": "user",
                "content": GIT_COMMIT_MESSAGE_USER_PROMPT.format(diff=diff),
            },
        ]

    def invoke(self, diff: str):
        messages = self._create_messages(diff)
        response = self._client.chat(model=self._model, messages=messages)
        return response["message"]["content"]

    def stream(self, diff: str):
        """
        Example usage:
        engine = OllamaEngine()
        diff = get_diff()
        for chunk in engine.stream(diff):
            print(chunk, end="", flush=True)
        """
        messages = self._create_messages(diff)
        response = self._client.chat(model=self._model, messages=messages, stream=True)
        for chunk in response:
            yield chunk["message"]["content"]
