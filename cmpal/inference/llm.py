from ollama import Client

from cmpal.inference.prompts import (
    GIT_COMMIT_MESSAGE_SYSTEM_PROMPT,
    GIT_COMMIT_MESSAGE_USER_PROMPT,
)


class OllamaEngine:
    def __init__(self, host="http://localhost:11434", model="llama3.2", config=None, headers=None):
        # TODO: Add default config to the constructor
        self._client = Client(host=host, headers=headers or {"x-some-header": "some-value"})
        self._model = model
        self._config = config

    def _create_messages(self, diff: str):
        return [
            {
                "role": "system",
                "content": GIT_COMMIT_MESSAGE_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": GIT_COMMIT_MESSAGE_USER_PROMPT.format(
                    diff=diff, style_config=self._config
                ),
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
