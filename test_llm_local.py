from llm.client import LLMClient


def main():
    client = LLMClient()

    prompt = """
Explique em português, em no máximo três frases,
por que a otimização de rotas pode ser importante
para entregas hospitalares.
""".strip()

    print("Sending prompt to local LLM...\n")

    response = client.generate(prompt)

    print("=== LLM Response ===")
    print(response)


if __name__ == "__main__":
    main()