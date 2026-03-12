from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME

client = Groq(api_key=GROQ_API_KEY)


def run_gap_agent(trend_summary, papers):

    paper_titles = "\n".join([p["title"] for p in papers[:10]])

    prompt = f"""
You are an expert research analyst.

Your task is to identify **ONLY 3 high-impact research gaps** using:

1. Emerging research trends
2. Citation relationships between papers

Emerging Research Trends:
{trend_summary}

Existing Papers:
{paper_titles}

Instructions:
- Identify **exactly 3 research gaps**
- Each gap must be **important and realistic**
- Focus on **under-explored intersections of technologies**
- Each summary must be **2–3 concise sentences**

Return STRICTLY in this format:

Title: <research gap title>
Summary: <2–3 sentence explanation>

Title: <research gap title>
Summary: <2–3 sentence explanation>

Title: <research gap title>
Summary: <2–3 sentence explanation>
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.choices[0].message.content

    gaps = []

    blocks = text.split("Title:")

    for b in blocks[1:]:

        parts = b.split("Summary:")

        title = parts[0].strip()

        summary = parts[1].strip() if len(parts) > 1 else ""

        gaps.append({
            "title": title,
            "summary": summary
        })

    return gaps[:3]