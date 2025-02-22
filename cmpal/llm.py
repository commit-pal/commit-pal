from ollama import Client


class OllamaEngine:
    def __init__(self, host="http://localhost:11434", model="llama3.2", headers=None):
        self._client = Client(host=host, headers=headers or {"x-some-header": "some-value"})
        self._model = model

    def _create_messages(self, prompt):
        return [
            {
                "role": "user",
                "content": prompt,
            }
        ]

    def invoke(self, prompt):
        messages = self._create_messages(prompt)
        response = self._client.chat(model=self._model, messages=messages)
        return response["message"]["content"]

    def stream(self, prompt):
        """
        Example usage:
        engine = OllamaEngine()
        for chunk in engine.stream('Hello, how are you?'):
            print(chunk, end='', flush=True)
        """
        messages = self._create_messages(prompt)
        response = self._client.chat(model=self._model, messages=messages, stream=True)
        for chunk in response:
            yield chunk["message"]["content"]
