from pyvis.network import Network
import tempfile


# ---------------------------------------------------
# Clean and validate year
# ---------------------------------------------------

def clean_year(y):

    # If already integer
    if isinstance(y, int):
        year = y

    else:
        try:
            year = int(str(y).strip())
        except:
            return None

    # Optional sanity range
    if year < 1990 or year > 2100:
        return None

    return year


# ---------------------------------------------------
# Build citation network
# ---------------------------------------------------

def build_citation_graph(papers):

    net = Network(
        height="600px",
        width="100%",
        bgcolor="#000000",
        font_color="white"
    )

    # -----------------------------
    # Add nodes
    # -----------------------------

    for i, paper in enumerate(papers):

        title = paper.get("title", "Paper")

        net.add_node(
            i,
            label=title[:35] + "...",
            title=title,
            color="#00FFFF"
        )

    # -----------------------------
    # Create pseudo citation edges
    # -----------------------------

    for i in range(len(papers)):
        for j in range(i + 1, len(papers)):

            year_i = clean_year(papers[i].get("year"))
            year_j = clean_year(papers[j].get("year"))

            # Skip invalid years
            if year_i is None or year_j is None:
                continue

            # Older papers cite newer ones
            if year_i <= year_j:
                net.add_edge(i, j)

    net.force_atlas_2based()

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")

    net.save_graph(tmp_file.name)

    return tmp_file.name