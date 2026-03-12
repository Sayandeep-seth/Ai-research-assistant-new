# Ai-research-assistant-new
An AI-powered research assistant built with Streamlit that automates the full academic workflow. Enter a topic → it fetches papers from ArXiv &amp; Semantic Scholar, analyzes trends, detects research gaps, designs methodology, writes a grant proposal (PDF export), and scores its novelty — all powered by LLaMA 3.3 70B via Groq.
#  AI Research Assistant

> An AI-powered academic research assistant that automates the full research workflow — from paper discovery to grant proposal generation — powered by **LLaMA 3.3 70B** via Groq.

---

##  Overview

Enter any research topic and the app runs a 6-stage automated pipeline:

1. **Literature Mining** — Fetches real papers from ArXiv & Semantic Scholar (parallel)
2. **Trend Analysis** — LLM identifies 5 emerging topics + interactive trend chart
3. **Research Gap Detection** — LLM surfaces 3 underexplored research opportunities
4. **Methodology Design** — LLM generates a structured experimental methodology
5. **Grant Proposal** — LLM writes a full 8-section proposal + exports as PDF
6. **Novelty Scoring** — Semantic embeddings score how original your proposal is (0–100)

---

##  Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| LLM | Groq API — LLaMA 3.3 70B Versatile |
| Paper Sources | ArXiv API + Semantic Scholar API |
| Embeddings | Sentence-Transformers `all-MiniLM-L6-v2` |
| Vector Database | ChromaDB |
| PDF Export | ReportLab |
| Charts | Plotly |
| Multi-Agent (alt) | CrewAI |

---

##  Project Structure

```
AI_Research_Assistant/
├── app.py                        # Main Streamlit app
├── config.py                     # API keys, model config, paths
├── requirements.txt              # Python dependencies
│
├── agents/
│   ├── literature_agent.py       # Calls paper fetcher
│   ├── trend_agent.py            # LLM trend extraction + Plotly chart
│   ├── gap_agent.py              # LLM research gap detection
│   ├── methodology_agent.py      # LLM methodology designer
│   ├── grant_agent.py            # LLM grant proposal writer
│   ├── novelty_agent.py          # Sentence-Transformer novelty scoring
│   ├── crew_agents.py            # CrewAI agent definitions
│   └── research_crew.py          # CrewAI crew orchestration
│
├── utils/
│   ├── paper_fetcher.py          # Parallel ArXiv + Semantic Scholar fetch
│   ├── pdf_generator.py          # ReportLab PDF converter
│   ├── citation_graph.py         # NetworkX citation graph
│   └── vector_store.py           # ChromaDB store/retrieve
│
├── rag/
│   ├── embeddings.py             # HuggingFace embeddings wrapper
│   ├── vector_store.py           # ChromaDB initialisation
│   └── retriever.py              # RAG retriever (reserved)
│
├── visualizations/
│   ├── trend_chart.py            # BERTopic bar chart
│   ├── gap_chart.py              # Reserved
│   └── novelty_chart.py          # Reserved
│
├── data/
│   └── vector_db/                # Persistent ChromaDB storage
│
└── .streamlit/
    └── config.toml               # Dark theme configuration
```

---

##  Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/ai-research-assistant.git
cd ai-research-assistant
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure your API key
Open `config.py` and replace the Groq API key:
```python
GROQ_API_KEY = "your_groq_api_key_here"
```
> Get a free API key at [console.groq.com](https://console.groq.com)

### 4. Run the app
```bash
streamlit run app.py
```

---

##  How to Use

1. Open the app in your browser (`http://localhost:8501`)
2. Type a research topic in the input field (e.g., `Federated Learning`)
3. Navigate through the tabs in order:
   - **Literature Mining** → wait for papers to load
   - **Trend Analysis** → view the emerging topics chart
   - **Research Gaps** → review the 3 identified gaps
   - **Methodology Design** → select a gap and click **Generate Methodology**
   - **Grant Proposal** → click **Generate Grant Proposal** → download PDF
   - **Novelty Scoring** → view your proposal's originality score

---

##  Pipeline Flow

```
User Input (topic)
      ↓
 Paper Fetcher ──── ArXiv API  ──┐
                                 ├──→ Merged & sorted papers
               ── Semantic Scholar ┘
      ↓
 Trend Agent ──→ LLM extracts 5 topics ──→ Plotly line chart
      ↓
 Gap Agent ──→ LLM identifies 3 research gaps
      ↓
 Methodology Agent ──→ LLM designs experiment (5 sections)
      ↓
 Grant Agent ──→ LLM writes proposal (8 sections) ──→ PDF export
      ↓
 Novelty Agent ──→ Cosine similarity ──→ Score (0–100 gauge)
```

---

##  Novelty Score Formula

```
novelty_score = 1 - (0.7 × avg_cosine_similarity_of_top_3_papers)
```

| Score Range | Meaning |
|---|---|
| 70–100 | Highly novel — strong original contribution |
| 40–70 | Moderate novelty — builds on existing work |
| 0–40 | Low novelty — closely mirrors existing research |

---

##  Key Dependencies

```
streamlit
groq
sentence-transformers
chromadb
langchain
langchain-community
plotly
reportlab
scikit-learn
crewai
networkx
arxiv
```

---

##  Roadmap

- [ ] Connect RAG retriever to enable question-answering over stored papers
- [ ] Wire CrewAI multi-agent pipeline to the Streamlit UI
- [ ] Add BERTopic-based topic modeling as an alternative to LLM extraction
- [ ] Implement citation graph visualization tab
- [ ] Add support for uploading custom PDFs to the vector store
- [ ] Export full research report (literature + gaps + methodology + grant) as one PDF

---

##  License

This project is licensed under the MIT License.

---

##  Acknowledgements

- [Groq](https://groq.com) for ultra-fast LLM inference
- [ArXiv](https://arxiv.org) & [Semantic Scholar](https://www.semanticscholar.org) for open paper APIs
- [Sentence-Transformers](https://www.sbert.net) for semantic embedding models
- [ChromaDB](https://www.trychroma.com) for the vector database
- [CrewAI](https://www.crewai.com) for the multi-agent framework
