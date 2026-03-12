from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_similarity_reason(grant_text, paper_summary, score):

    grant_words = set(grant_text.lower().split())
    paper_words = set(paper_summary.lower().split())

    common_words = list(grant_words.intersection(paper_words))

    if len(common_words) > 0:
        keyword = common_words[0]
    else:
        keyword = "the research topic"

    if score > 0.75:
        return (
            f"This paper strongly relates to the proposed research, particularly around {keyword}. "
            f"The research objectives and methodology show significant overlap."
        )

    elif score > 0.55:
        return (
            f"This work discusses concepts related to {keyword} within the same research area. "
            f"There is moderate similarity in techniques or application domain."
        )

    else:
        return (
            f"This paper belongs to the broader field connected to {keyword}. "
            f"However, its specific methods differ from the proposed research."
        )


def compute_similarity(grant_text, papers):

    grant_embedding = model.encode([grant_text])

    paper_texts = [p["summary"] for p in papers[:10]]

    paper_embeddings = model.encode(paper_texts)

    sims = cosine_similarity(grant_embedding, paper_embeddings)[0]

    results = []

    for i, score in enumerate(sims):

        explanation = generate_similarity_reason(
            grant_text,
            papers[i]["summary"],
            score
        )

        results.append({
            "title": papers[i]["title"],
            "link": papers[i]["link"],
            "score": float(score),
            "explanation": explanation
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    top_k = results[:3]

    avg_sim = np.mean([r["score"] for r in top_k])

    novelty_score = 1 - (0.7 * avg_sim)

    novelty_percent = novelty_score * 100

    return novelty_percent, top_k