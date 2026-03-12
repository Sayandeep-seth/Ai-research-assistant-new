import plotly.express as px

def plot_trends(topic_info):

    topic_info = topic_info[topic_info["Topic"] != -1]

    fig = px.bar(
        topic_info,
        x="Topic",
        y="Count",
        color="Count",
        title="Research Topic Distribution",
    )

    fig.update_layout(
        template="plotly_dark",
        height=500
    )

    return fig