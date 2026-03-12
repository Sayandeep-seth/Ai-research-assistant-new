import streamlit as st
import plotly.graph_objects as go
from utils.pdf_generator import create_pdf

st.set_page_config(page_title="AI Research Assistant", layout="wide")

# ---------------------------------------------------
# SESSION STATE VARIABLES
# ---------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "Literature Mining"

if "topic_input" not in st.session_state:
    st.session_state.topic_input = ""

if "search_history" not in st.session_state:
    st.session_state.search_history = []

if "reset_input" not in st.session_state:
    st.session_state.reset_input = False

if "papers" not in st.session_state:
    st.session_state.papers = None

if "trend_summary" not in st.session_state:
    st.session_state.trend_summary = None

if "trend_fig" not in st.session_state:
    st.session_state.trend_fig = None

if "gaps" not in st.session_state:
    st.session_state.gaps = None

if "methodology" not in st.session_state:
    st.session_state.methodology = None

if "grant" not in st.session_state:
    st.session_state.grant = None

if "novelty" not in st.session_state:
    st.session_state.novelty = None

if "grant_suggestion" not in st.session_state:
    st.session_state.grant_suggestion = None


# ---------------------------------------------------
# RESET FUNCTION
# ---------------------------------------------------

def reset_session():
    st.session_state.papers = None
    st.session_state.trend_summary = None
    st.session_state.trend_fig = None
    st.session_state.gaps = None
    st.session_state.methodology = None
    st.session_state.grant = None
    st.session_state.novelty = None
    st.session_state.grant_suggestion = None


# ---------------------------------------------------
# HANDLE INPUT RESET
# ---------------------------------------------------

if st.session_state.reset_input:
    st.session_state.topic_input = ""
    st.session_state.reset_input = False


# ---------------------------------------------------
# SIDEBAR DASHBOARD
# ---------------------------------------------------

with st.sidebar:

    st.title("AI Research Assistant")

    progress = 0

    if st.session_state.papers:
        progress = 20

    if st.session_state.trend_summary:
        progress = 40

    if st.session_state.gaps:
        progress = 60

    if st.session_state.methodology:
        progress = 80

    if st.session_state.grant:
        progress = 100

    st.subheader("Research Progress")
    st.progress(progress / 100)
    st.caption(f"{progress}% Complete")

    st.divider()

    st.subheader("Dashboard")

    if st.button("📚 Literature Mining", use_container_width=True):
        st.session_state.page = "Literature Mining"

    if st.button("📈 Trend Analysis", use_container_width=True):
        st.session_state.page = "Trend Analysis"

    if st.button("🧠 Research Gaps", use_container_width=True):
        st.session_state.page = "Research Gaps"

    if st.button("⚙ Methodology Design", use_container_width=True):
        st.session_state.page = "Methodology Design"

    if st.button("💰 Grant Proposal", use_container_width=True):
        st.session_state.page = "Grant Proposal"

    if st.button("🔬 Novelty Scoring", use_container_width=True):
        st.session_state.page = "Novelty Scoring"


# ---------------------------------------------------
# UI STYLE
# ---------------------------------------------------

st.markdown("""
<style>

.main-title{
font-size:42px;
font-weight:700;
text-align:center;
background: linear-gradient(90deg,#00C9FF,#92FE9D);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
margin-bottom:25px;
}

.input-card{
background:rgba(255,255,255,0.05);
padding:20px;
border-radius:15px;
box-shadow:0px 4px 20px rgba(0,0,0,0.1);
margin-bottom:20px;
}

.stButton>button{
border-radius:10px;
height:45px;
font-weight:600;
}

</style>
""", unsafe_allow_html=True)


st.markdown(
"""
<div class="main-title">
AI Research Assistant & Grant Proposal Generator
</div>
""",
unsafe_allow_html=True
)

# ---------------------------------------------------
# INPUT CARD
# ---------------------------------------------------

st.markdown('<div class="input-card">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([6,1,1])

with col1:

    topic = st.selectbox(
        "Enter Research Topic",
        options=st.session_state.search_history if st.session_state.search_history else [""],
        index=None,
        placeholder="Example: AI for Healthcare Diagnosis",
        key="topic_input",
        accept_new_options=True
    )

with col2:

    if st.button("🔄 Refresh", use_container_width=True):
        reset_session()
        st.session_state.reset_input = True
        st.rerun()

with col3:

    if st.button("▶ Rerun", use_container_width=True):
        reset_session()
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------
# SAVE SEARCH HISTORY
# ---------------------------------------------------

if topic:

    if topic not in st.session_state.search_history:
        st.session_state.search_history.append(topic)


# ---------------------------------------------------
# CACHE FUNCTIONS
# ---------------------------------------------------

@st.cache_data(show_spinner=False)
def fetch_papers(topic):
    from agents.literature_agent import run_literature_agent
    return run_literature_agent(topic)

@st.cache_data(show_spinner=False)
def compute_trends(papers):
    from agents.trend_agent import run_trend_agent
    return run_trend_agent(papers)

@st.cache_data(show_spinner=False)
def detect_gaps(summary, papers):
    from agents.gap_agent import run_gap_agent
    return run_gap_agent(summary, papers)

@st.cache_data(show_spinner=False)
def compute_novelty(grant, papers):
    from agents.novelty_agent import compute_similarity
    return compute_similarity(grant, papers)


# ===================================================
# PAGE 1 — LITERATURE MINING
# ===================================================

if st.session_state.page == "Literature Mining":

    if topic:

        if st.session_state.papers is None:

            with st.spinner("Fetching research papers..."):
                st.session_state.papers = fetch_papers(topic)

        papers = st.session_state.papers

        for p in papers:

            st.markdown(f"""
### {p['title']}

**Year:** {p['year']}  
**Source:** {p['source']}

{p['summary']}

[Read Paper]({p['link']})

---
""")


# ===================================================
# PAGE 2 — TREND ANALYSIS
# ===================================================

elif st.session_state.page == "Trend Analysis":

    papers = st.session_state.papers

    if papers:

        if st.session_state.trend_fig is None:

            with st.spinner("Analyzing research trends..."):

                summary, fig = compute_trends(papers)

                st.session_state.trend_summary = summary
                st.session_state.trend_fig = fig

        st.subheader("Emerging Research Trends")

        st.write(st.session_state.trend_summary)

        st.plotly_chart(
            st.session_state.trend_fig,
            use_container_width=True
        )

    else:
        st.warning("Please fetch literature first.")


# ===================================================
# PAGE 3 — RESEARCH GAPS
# ===================================================

elif st.session_state.page == "Research Gaps":

    summary = st.session_state.trend_summary
    papers = st.session_state.papers

    if summary and papers:

        st.subheader("Citation Network Graph")

        from utils.citation_graph import build_citation_graph

        graph_html = build_citation_graph(papers)

        with open(graph_html, "r", encoding="utf-8") as f:
            html = f.read()

        st.components.v1.html(html, height=650, scrolling=True)

        if st.session_state.gaps is None:

            with st.spinner("Identifying research gaps..."):
                st.session_state.gaps = detect_gaps(summary, papers)

        gaps = st.session_state.gaps

        st.subheader("Detected Research Gaps")

        for g in gaps:

            st.markdown(f"""
### **{g['title']}**

{g['summary']}

---
""")

    else:
        st.warning("Please complete Literature Mining and Trend Analysis first.")


# ===================================================
# PAGE 4 — METHODOLOGY DESIGN
# ===================================================

elif st.session_state.page == "Methodology Design":

    gaps = st.session_state.gaps

    if gaps:

        st.subheader("Select Research Gap")

        gap_titles = [g["title"] for g in gaps]

        selected_gap = st.radio(
            "Choose one of the research gaps",
            gap_titles
        )

        custom_gap = st.text_area("Or enter your own research gap")

        if st.button("Generate Methodology"):

            gap_input = custom_gap if custom_gap else selected_gap

            from agents.methodology_agent import run_methodology_agent

            with st.spinner("Designing research methodology..."):

                methodology = run_methodology_agent(gap_input)

            st.session_state.methodology = methodology

        if st.session_state.methodology:

            st.subheader("Generated Methodology")

            st.markdown(st.session_state.methodology)

    else:
        st.warning("Please detect research gaps first.")


# ===================================================
# PAGE 5 — GRANT PROPOSAL
# ===================================================

elif st.session_state.page == "Grant Proposal":

    methodology = st.session_state.methodology

    if methodology:

        st.subheader("Generated Methodology")
        st.markdown(methodology)

        custom_method = st.text_area("Or enter custom methodology")

        if topic and st.session_state.grant_suggestion is None:

            from agents.grant_agent import suggest_grant_program

            with st.spinner("Analyzing best funding program..."):

                st.session_state.grant_suggestion = suggest_grant_program(topic)

        if st.session_state.grant_suggestion:
            st.info(st.session_state.grant_suggestion)

        grant_format = st.selectbox(
            "Select Grant Proposal Format (Optional)",
            [
                "Default",
                "NSF Grant Proposal Format",
                "NIH Grant Proposal Format",
                "Horizon Europe / EU Grant Format",
                "SBIR / Startup Innovation Grant Format",
                "General Academic Grant Proposal Format"
            ]
        )

        if st.button("Generate Grant Proposal"):

            method_input = custom_method if custom_method else methodology

            from agents.grant_agent import run_grant_agent

            with st.spinner("Writing grant proposal..."):

                grant = run_grant_agent(method_input, grant_format)

            st.session_state.grant = grant

        if st.session_state.grant:

            st.subheader("Generated Grant Proposal")

            st.markdown(st.session_state.grant)

            create_pdf(st.session_state.grant, "grant.pdf")

            with open("grant.pdf", "rb") as f:

                st.download_button(
                    "Download Grant PDF",
                    f,
                    "grant_proposal.pdf"
                )

    else:
        st.warning("Please generate methodology first.")


# ===================================================
# PAGE 6 — NOVELTY SCORING
# ===================================================

elif st.session_state.page == "Novelty Scoring":

    grant = st.session_state.grant
    papers = st.session_state.papers

    if grant and papers:

        if st.session_state.novelty is None:

            with st.spinner("Computing novelty score..."):

                novelty_score, results = compute_novelty(grant, papers)

            st.session_state.novelty = (novelty_score, results)

        novelty_score, results = st.session_state.novelty

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=round(novelty_score,2),
            title={"text": "Novelty Score (%)"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "cyan"},
                "steps": [
                    {"range": [0, 35], "color": "red"},
                    {"range": [35, 75], "color": "yellow"},
                    {"range": [75, 100], "color": "green"}
                ]
            }
        ))

        st.plotly_chart(fig)

        st.subheader("Novelty Interpretation")

        if novelty_score < 35:
            st.error("Low Novelty — similar research already exists.")
        elif novelty_score < 75:
            st.warning("Moderate Novelty — partially explored research area.")
        else:
            st.success("High Novelty — strong research contribution.")

        st.subheader("Existing Papers Similar to the Topic")

        for r in results:

            st.markdown(f"### {r['title']}")
            st.markdown(f"**Similarity Score:** {float(r['score']):.2f}")

            if "explanation" in r:
                st.markdown(r["explanation"])

            st.markdown(f"[Read Paper]({r['link']})")
            st.markdown("---")

    else:
        st.warning("Please generate a grant proposal first.")