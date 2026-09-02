from llm.client import LLMClient
from llm.prompts import (
    build_driver_instructions_prompt,
    build_improvement_prompt,
    build_question_prompt,
    build_route_report_prompt,
)
from llm.context import build_summary_context


class LLMService:
    def __init__(
        self,
        client: LLMClient | None = None,
    ):
        self.client = client or LLMClient()

    def generate_driver_instructions(
        self,
        context: dict,
    ) -> str:
        prompt = build_driver_instructions_prompt(
            context
        )

        return self.client.generate(prompt)

    def generate_route_report(
        self,
        context: dict,
        period: str = "daily",
    ) -> str:
        summary_context = build_summary_context(
            context
        )

        prompt = build_route_report_prompt(
            summary_context,
            period=period,
        )

        llm_report = self.client.generate(prompt)

        if self._route_report_is_safe(llm_report):
            return llm_report

        return self._build_factual_route_report(
            summary_context,
            period,
        )

    def suggest_route_improvements(
        self,
        context: dict,
    ) -> str:
        prompt = build_improvement_prompt(
            context
        )

        return self.client.generate(prompt)

    def answer_route_question(
        self,
        context: dict,
        question: str,
    ) -> str:
        prompt = build_question_prompt(
            context,
            question,
        )

        return self.client.generate(prompt)

    @staticmethod
    def _route_report_is_safe(
        report: str,
    ) -> bool:
        normalized = report.lower()

        forbidden_terms = (
            " km",
            "quilômetro",
            "quilometro",
            "signific",
            "efici",
            "benéfic",
            "economia de combustível",
            "economia de combustivel",
            "economia financeira",
            "redução de custos",
            "reducao de custos",
            "base linha",
        )

        return not any(
            term in normalized
            for term in forbidden_terms
        )

    @staticmethod
    def _build_factual_route_report(
        summary: dict,
        period: str,
    ) -> str:
        optimized = summary["optimized"]
        baseline = summary.get("baseline")
        comparison = summary.get(
            "comparison",
            {},
        )

        period_label = {
            "daily": "diário",
            "weekly": "semanal",
        }.get(period, period)

        lines = [
            (
                "Relatório de otimização de rotas "
                f"{period_label}"
            ),
            "",
            "Solução otimizada:",
            (
                "- Distância: "
                f"{optimized['distance']:.2f} "
                "unidades de distância"
            ),
            (
                "- Fitness: "
                f"{optimized['fitness']:.2f}"
            ),
            (
                "- Penalidade de prioridade: "
                f"{optimized['priority_penalty']:.2f}"
            ),
            (
                "- Penalidade de autonomia: "
                f"{optimized['autonomy_penalty']:.2f}"
            ),
            (
                "- Número de rotas: "
                f"{optimized['routes']}"
            ),
        ]

        if baseline is not None:
            lines.extend(
                [
                    "",
                    (
                        "Comparação com a solução "
                        "de referência (baseline):"
                    ),
                ]
            )

            metrics = (
                (
                    "Fitness",
                    "fitness_difference_percent",
                    "fitness_change",
                ),
                (
                    "Distância",
                    "distance_difference_percent",
                    "distance_change",
                ),
                (
                    "Penalidade de prioridade",
                    "priority_penalty_difference_percent",
                    "priority_penalty_change",
                ),
            )

            direction_labels = {
                "lower": "menor",
                "higher": "maior",
                "unchanged": "inalterado",
            }

            for (
                label,
                percentage_key,
                change_key,
            ) in metrics:
                if percentage_key not in comparison:
                    continue

                percentage = comparison[
                    percentage_key
                ]
                direction = direction_labels.get(
                    comparison.get(change_key),
                    comparison.get(
                        change_key,
                        "não especificado",
                    ),
                )

                lines.append(
                    f"- {label}: "
                    f"{abs(percentage):.2f}% "
                    f"{direction}"
                )

        lines.extend(
            [
                "",
                "Observações operacionais:",
                (
                    "- Os valores de distância "
                    "estão em unidades de distância "
                    "da simulação."
                ),
            ]
        )

        if optimized["autonomy_penalty"] == 0:
            lines.append(
                "- Nenhuma penalidade por excesso "
                "de autonomia foi aplicada."
            )

        return "\n".join(lines)