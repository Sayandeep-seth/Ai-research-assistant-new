import networkx as nx
import plotly.graph_objects as go
from sklearn.feature_extraction.text import TfidfVectorizer


def build_topic_network(papers):

    texts = [p["summary"] for p in papers]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=25
    )

    X = vectorizer.fit_transform(texts)

    keywords = vectorizer.get_feature_names_out()

    G = nx.Graph()

    for word in keywords:
        G.add_node(word)

    for i in range(len(keywords)):
        for j in range(i + 1, len(keywords)):

            weight = (X[:, i].multiply(X[:, j])).sum()

            if weight > 0:
                G.add_edge(keywords[i], keywords[j], weight=float(weight))

    pos = nx.spring_layout(G, seed=42)

    edge_x = []
    edge_y = []

    for edge in G.edges():

        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    node_x = []
    node_y = []
    text = []

    for node in G.nodes():

        x, y = pos[node]

        node_x.append(x)
        node_y.append(y)
        text.append(node)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=text,
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            size=20,
            color='cyan',
            line_width=2
        )
    )

    fig = go.Figure(data=[edge_trace, node_trace])

    fig.update_layout(
        showlegend=False,
        margin=dict(l=20,r=20,t=20,b=20),
        paper_bgcolor="black",
        plot_bgcolor="black"
    )

    return fig