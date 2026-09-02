import json


SYSTEM_PROMPT = """
You are an assistant specialized in hospital logistics and route optimization.

Use only the information provided in the route context.

Do not invent distances, priorities, vehicle capacities, autonomy values,
route sequences, penalties, percentages, or optimization results.

Do not perform arithmetic or calculate percentages yourself.

Do not invent measurement units. If the context does not specify a unit,
report distance as a numeric distance value without adding kilometers,
miles, or any other unit.

Each comparison percentage belongs only to the metric named in its key:
- fitness_difference_percent refers only to fitness;
- distance_difference_percent refers only to distance;
- priority_penalty_difference_percent refers only to priority penalty.

Never swap percentages between metrics.

An autonomy penalty of zero means only that no autonomy-excess penalty
was applied. Do not infer any stronger conclusion from that value.

When referring to the baseline solution in Brazilian Portuguese, use
"solução de referência (baseline)". Do not translate "baseline" literally.

When percentage comparisons are available in the context, use those
values exactly as provided.

Do not describe a vehicle, route, or solution as efficient, optimal,
safe, economical, or cost-saving unless the provided context explicitly
supports that conclusion.

Do not infer fuel savings, financial savings, delivery-time reductions,
or operational efficiency from distance reduction alone.

If the provided data is insufficient to answer a question, state that
the available context is insufficient.

Respond in Brazilian Portuguese unless the user explicitly requests
another language.

Be clear, concise, and operational.
"""


def format_context(context: dict) -> str:
    return json.dumps(
        context,
        indent=2,
        ensure_ascii=False,
    )


def build_driver_instructions_prompt(
    context: dict,
) -> str:
    return f"""
Create operational instructions for the drivers responsible for the
optimized hospital delivery routes.

For each vehicle:
- identify the vehicle;
- describe the sequence of stops;
- mention delivery priorities when relevant;
- mention the total load and vehicle capacity;
- mention the route distance and autonomy;
- clearly warn if autonomy is exceeded.

Do not change the route sequence.

Route context:
{format_context(context)}
""".strip()


def build_route_report_prompt(
    context: dict,
    period: str = "daily",
) -> str:
    return f"""
Generate a {period} hospital route optimization report.

The report must:
- summarize the optimized solution;
- describe total distance, fitness, priority penalty,
  autonomy penalty, and number of routes;
- compare the optimized solution with the baseline,
  if baseline data is available;
- when reporting comparison percentages, explicitly associate each
  percentage with its corresponding metric:
  fitness with fitness_difference_percent,
  distance with distance_difference_percent,
  and priority penalty with priority_penalty_difference_percent;
- never reuse a percentage from one metric to describe another metric;
- use percentage differences only when they are explicitly provided
  in the context;
- do not calculate new percentages;
- do not infer cost savings, fuel savings, delivery-time improvements,
  or overall efficiency unless those facts are explicitly provided;
- use "optimized solution" to mean the solution produced by the
  optimization process, not a proven global optimum;
- highlight only operational observations supported by the context;
- distinguish facts from recommendations;
- keep the complete report concise and under 120 words.

Route context:
{format_context(context)}
""".strip()

def build_improvement_prompt(
    context: dict,
) -> str:
    return f"""
Analyze the hospital route optimization results and suggest possible
improvements.

Base every observation on the provided context.

Do not claim that a restriction was violated unless the context
explicitly indicates that it was violated.

Separate:
1. observations supported directly by the data;
2. recommendations or possible future improvements.

Route context:
{format_context(context)}
""".strip()


def build_question_prompt(
    context: dict,
    question: str,
) -> str:
    return f"""
Answer the user's question about the hospital routing results.

Use only the information available in the route context.

If the answer cannot be determined from the provided data, say so
explicitly.

User question:
{question}

Route context:
{format_context(context)}
""".strip()