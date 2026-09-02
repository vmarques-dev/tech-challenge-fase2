from llm.service import LLMService


class FakeLLMClient:
    def __init__(self):
        self.last_prompt = None

    def generate(
        self,
        prompt: str,
    ) -> str:
        self.last_prompt = prompt
        return "Generated response"


def build_test_context():
    return {
        "optimized": {
            "fitness": 100.0,
            "distance": 50.0,
            "priority_penalty": 50.0,
            "autonomy_penalty": 0.0,
            "routes": 1,
        },
        "route_details": [
            {
                "vehicle": "Vehicle 1",
                "capacity": 100.0,
                "load": 50.0,
                "autonomy": 1000.0,
                "distance": 50.0,
                "autonomy_exceeded": False,
                "stops": [
                    {
                        "name": "Base",
                        "priority": 1,
                        "demand": 0.0,
                    },
                    {
                        "name": "Hospital A",
                        "priority": 3,
                        "demand": 50.0,
                    },
                ],
            }
        ],
    }


def test_generate_driver_instructions():
    client = FakeLLMClient()
    service = LLMService(client=client)

    result = service.generate_driver_instructions(
        build_test_context()
    )

    assert result == "Generated response"
    assert "Vehicle 1" in client.last_prompt
    assert "operational instructions" in client.last_prompt


def test_generate_route_report():
    client = FakeLLMClient()
    service = LLMService(client=client)

    result = service.generate_route_report(
        build_test_context(),
        period="weekly",
    )

    assert result == "Generated response"
    assert "weekly" in client.last_prompt
    assert "hospital route optimization report" in client.last_prompt


def test_suggest_route_improvements():
    client = FakeLLMClient()
    service = LLMService(client=client)

    result = service.suggest_route_improvements(
        build_test_context()
    )

    assert result == "Generated response"
    assert "suggest possible" in client.last_prompt
    assert "recommendations" in client.last_prompt


def test_answer_route_question():
    client = FakeLLMClient()
    service = LLMService(client=client)

    question = "Was vehicle autonomy exceeded?"

    result = service.answer_route_question(
        build_test_context(),
        question,
    )

    assert result == "Generated response"
    assert question in client.last_prompt
    assert "autonomy_exceeded" in client.last_prompt