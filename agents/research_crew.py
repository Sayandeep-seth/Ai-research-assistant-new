from crewai import Task, Crew

from agents.crew_agents import (
    trend_agent,
    gap_agent,
    novelty_agent,
    methodology_agent,
    grant_agent
)

from rag.rag_pipeline import build_rag_context


def run_research_pipeline(user_topic):

    # Build RAG Context
    context = build_rag_context(user_topic)

    trend_task = Task(
        description=f"""
        Analyze research trends for topic: {user_topic}

        Context from literature:
        {context}
        """,
        agent=trend_agent
    )

    gap_task = Task(
        description=f"""
        Identify research gaps for topic: {user_topic}

        Context from literature:
        {context}
        """,
        agent=gap_agent
    )

    novelty_task = Task(
        description=f"""
        Generate novel research ideas for topic: {user_topic}

        Context from literature:
        {context}
        """,
        agent=novelty_agent
    )

    methodology_task = Task(
        description=f"""
        Design research methodology for topic: {user_topic}

        Context from literature:
        {context}
        """,
        agent=methodology_agent
    )

    grant_task = Task(
        description=f"""
        Write a grant proposal for topic: {user_topic}

        Context from literature:
        {context}
        """,
        agent=grant_agent
    )

    crew = Crew(
        agents=[
            trend_agent,
            gap_agent,
            novelty_agent,
            methodology_agent,
            grant_agent
        ],
        tasks=[
            trend_task,
            gap_task,
            novelty_task,
            methodology_task,
            grant_task
        ],
        verbose=True
    )

    result = crew.kickoff()

    return result