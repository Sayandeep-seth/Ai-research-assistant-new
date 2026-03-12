from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME

client = Groq(api_key=GROQ_API_KEY)


def run_methodology_agent(research_gap):

    prompt = f"""
You are a research methodology expert.

Design a concise experimental methodology for the following research gap.

Research Gap:
{research_gap}

Return the methodology in the following structured format:

1. Dataset
Mention 1–2 suitable datasets.

2. Model / Algorithm
Suggest appropriate models or techniques.

3. Experimental Setup
Describe the training setup and architecture briefly.

4. Evaluation Metrics
List relevant evaluation metrics.

5. Baseline Methods
Mention 2 baseline approaches for comparison.

Rules:
- Be concise
- Use bullet points
- Keep response under 180 words
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    methodology = response.choices[0].message.content.strip()

    return methodology