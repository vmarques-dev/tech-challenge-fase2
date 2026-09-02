import json
import urllib.error
import urllib.request

from llm.prompts import SYSTEM_PROMPT


DEFAULT_MODEL = "llama3.2:3b"
DEFAULT_BASE_URL = "http://localhost:11434"


class LLMClient:
    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = 300,
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def generate(
        self,
        prompt: str,
    ) -> str:
        payload = {
            "model": self.model,
            "system": SYSTEM_PROMPT,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_predict": 300,
            },
        }

        request_data = json.dumps(
            payload
        ).encode("utf-8")

        request = urllib.request.Request(
            url=f"{self.base_url}/api/generate",
            data=request_data,
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(
                request,
                timeout=self.timeout,
            ) as response:
                response_data = json.loads(
                    response.read().decode("utf-8")
                )


        except TimeoutError as error:

            raise RuntimeError(

                "The local Ollama model took too long to respond."

            ) from error


        except urllib.error.URLError as error:

            raise RuntimeError(

                "Could not connect to the local Ollama service."

            ) from error

        generated_text = response_data.get(
            "response",
            ""
        ).strip()

        if not generated_text:
            raise RuntimeError(
                "Ollama returned an empty response."
            )

        return generated_text