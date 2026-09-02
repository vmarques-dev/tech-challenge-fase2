from llm.prompts import (
    SYSTEM_PROMPT,
    build_driver_instructions_prompt,
    build_improvement_prompt,
    build_question_prompt,
    build_route_report_prompt,
)


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


def test_system_prompt_prevents_invented_data():
    assert "Do not invent" in SYSTEM_PROMPT
    assert "Use only" in SYSTEM_PROMPT
    assert "Do not perform arithmetic" in SYSTEM_PROMPT
    assert "calculate percentages" in SYSTEM_PROMPT
    assert "cost-saving" in SYSTEM_PROMPT
    assert "Brazilian Portuguese" in SYSTEM_PROMPT


def test_driver_prompt_contains_route_data():
    context = build_test_context()

    prompt = build_driver_instructions_prompt(
        context
    )

    assert "Vehicle 1" in prompt
    assert "Hospital A" in prompt
    assert "1000.0" in prompt


def test_report_prompt_contains_period_and_metrics():
    context = build_test_context()

    prompt = build_route_report_prompt(
        context,
        period="weekly",
    )

    assert "weekly" in prompt
    assert "fitness" in prompt
    assert "priority_penalty" in prompt
    assert "do not calculate new percentages" in prompt
    assert "do not infer cost savings" in prompt
    assert "not a proven global optimum" in prompt


def test_improvement_prompt_distinguishes_facts_and_recommendations():
    context = build_test_context()

    prompt = build_improvement_prompt(
        context
    )

    assert "observations" in prompt
    assert "recommendations" in prompt


def test_question_prompt_contains_question_and_context():
    context = build_test_context()

    question = "Was vehicle autonomy exceeded?"

    prompt = build_question_prompt(
        context,
        question,
    )

    assert question in prompt
    assert "autonomy_exceeded" in prompt