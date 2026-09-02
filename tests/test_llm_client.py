import json
import urllib.error

import pytest

from llm.client import (
    DEFAULT_BASE_URL,
    DEFAULT_MODEL,
    LLMClient,
)


class FakeResponse:
    def __init__(
        self,
        data: dict,
    ):
        self.data = data

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        return False

    def read(self):
        return json.dumps(
            self.data
        ).encode("utf-8")


def test_llm_client_uses_local_ollama_defaults():
    client = LLMClient()

    assert client.model == DEFAULT_MODEL
    assert client.model == "llama3.2:3b"

    assert client.base_url == DEFAULT_BASE_URL
    assert client.base_url == "http://localhost:11434"


def test_llm_client_generates_text(
    monkeypatch,
):
    def fake_urlopen(
        request,
        timeout,
    ):
        return FakeResponse(
            {
                "response": "Test response",
            }
        )

    monkeypatch.setattr(
        "urllib.request.urlopen",
        fake_urlopen,
    )

    client = LLMClient()

    result = client.generate(
        "Test prompt"
    )

    assert result == "Test response"


def test_llm_client_raises_error_when_ollama_is_unavailable(
    monkeypatch,
):
    def fake_urlopen(
        request,
        timeout,
    ):
        raise urllib.error.URLError(
            "Connection refused"
        )

    monkeypatch.setattr(
        "urllib.request.urlopen",
        fake_urlopen,
    )

    client = LLMClient()

    with pytest.raises(
        RuntimeError,
        match="Could not connect",
    ):
        client.generate(
            "Test prompt"
        )


def test_llm_client_rejects_empty_response(
    monkeypatch,
):
    def fake_urlopen(
        request,
        timeout,
    ):
        return FakeResponse(
            {
                "response": "",
            }
        )

    monkeypatch.setattr(
        "urllib.request.urlopen",
        fake_urlopen,
    )

    client = LLMClient()

    with pytest.raises(
        RuntimeError,
        match="empty response",
    ):
        client.generate(
            "Test prompt"
        )

def test_llm_client_raises_error_on_timeout(
    monkeypatch,
):
    def fake_urlopen(
        request,
        timeout,
    ):
        raise TimeoutError()

    monkeypatch.setattr(
        "urllib.request.urlopen",
        fake_urlopen,
    )

    client = LLMClient()

    with pytest.raises(
        RuntimeError,
        match="took too long",
    ):
        client.generate(
            "Test prompt"
        )