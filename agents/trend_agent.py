from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME
import plotly.graph_objects as go

client = Groq(api_key=GROQ_API_KEY)


# ---------------------------------------------------
# Extract high-quality emerging topics using LLM
# ---------------------------------------------------

def extract_topics_llm(papers):

    text_data = []

    for p in papers[:15]:

        title = str(p.get("title", ""))
        summary = str(p.get("summary", ""))

        text_data.append(title + " : " + summary)

    corpus = "\n".join(text_data)

    prompt = f"""
You are an AI research analyst.

From the following research paper titles and abstracts:

{corpus}

Identify the **5 most important emerging research topics**.

Rules:
- Only meaningful technical topics
- Avoid generic words like data, models, systems
- Prefer phrases like:
  Graph Neural Networks
  Explainable AI
  Federated Learning
  Multimodal LLMs
  Edge AI
  Reinforcement Learning

Return only the topics as a list.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    output = response.choices[0].message.content

    topics = []

    for line in output.split("\n"):

        line = line.strip("- ").strip()

        if line:
            topics.append(line)

    return topics[:5]


# ---------------------------------------------------
# Validate and clean year
# ---------------------------------------------------

def clean_year(raw_year):

    # Step 1: if already integer
    if isinstance(raw_year, int):
        year = raw_year

    else:
        # Step 2: attempt conversion
        try:
            year = int(str(raw_year).strip())
        except:
            return None

    # Step 3: validate realistic range
    if year < 1990 or year > 2100:
        return None

    return year


# ---------------------------------------------------
# Build topic vs year matrix
# ---------------------------------------------------

def build_topic_year_matrix(papers, topics):

    matrix = {t:{} for t in topics}

    for p in papers:

        raw_year = p.get("year")

        year = clean_year(raw_year)

        if year is None:
            continue

        title = str(p.get("title", ""))
        summary = str(p.get("summary", ""))

        text = (title + " " + summary).lower()

        for t in topics:

            words = t.lower().split()

            if any(w in text for w in words):

                matrix[t][year] = matrix[t].get(year, 0) + 1

    return matrix


# ---------------------------------------------------
# Generate colorful trend chart
# ---------------------------------------------------

def build_trend_chart(matrix):

    colors = [
        "#00D4FF",
        "#FF6B6B",
        "#FFD93D",
        "#6BCB77",
        "#9D4EDD"
    ]

    fig = go.Figure()

    for i, (topic, data) in enumerate(matrix.items()):

        if not data:
            continue

        years = sorted(data.keys())
        counts = [data[y] for y in years]

        fig.add_trace(

            go.Scatter(
                x=years,
                y=counts,
                mode="lines+markers",
                name=topic,
                line=dict(width=3, color=colors[i % len(colors)]),
                marker=dict(size=8)
            )

        )

    fig.update_layout(

        template="plotly_dark",
        title="Evolution of Emerging Research Topics",
        xaxis_title="Year",
        yaxis_title="Number of Papers",
        height=520,
        hovermode="x unified"
    )

    return fig


# ---------------------------------------------------
# Generate trend summary
# ---------------------------------------------------

def generate_summary(topics):

    if not topics:
        return "No emerging research topics detected."

    return f"""
Recent literature shows increasing academic attention toward **{", ".join(topics)}**.  

These areas represent the most active emerging research directions identified from the analyzed papers.  

The growing publication volume suggests strong momentum and interdisciplinary applications in these fields.  

Future research is likely to focus on scalable implementations and real-world deployment of these technologies.
"""


# ---------------------------------------------------
# Main Trend Agent
# ---------------------------------------------------

def run_trend_agent(papers):

    if not papers:
        return "No papers available for trend analysis.", go.Figure()

    topics = extract_topics_llm(papers)

    matrix = build_topic_year_matrix(papers, topics)

    fig = build_trend_chart(matrix)

    summary = generate_summary(topics)

    return summary, fig