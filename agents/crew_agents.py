from crewai import Agent
from langchain.chat_models import ChatOpenAI


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3
)


trend_agent = Agent(
    role="Research Trend Analyst",
    goal="Analyze emerging research trends",
    backstory="Expert in bibliometric analysis and research evolution",
    llm=llm,
    verbose=True
)


gap_agent = Agent(
    role="Research Gap Identifier",
    goal="Identify research gaps in the literature",
    backstory="Expert in detecting missing problems and unexplored areas",
    llm=llm,
    verbose=True
)


novelty_agent = Agent(
    role="Novel Research Idea Generator",
    goal="Generate innovative research ideas",
    backstory="Creative researcher capable of proposing novel approaches",
    llm=llm,
    verbose=True
)


methodology_agent = Agent(
    role="Research Methodology Designer",
    goal="Design detailed experimental methodologies",
    backstory="Expert in experimental design and scientific evaluation",
    llm=llm,
    verbose=True
)


grant_agent = Agent(
    role="Grant Proposal Writer",
    goal="Write compelling research grant proposals",
    backstory="Expert academic grant proposal writer",
    llm=llm,
    verbose=True
)