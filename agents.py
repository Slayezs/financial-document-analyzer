# agents.py

import os
from dotenv import load_dotenv
from crewai import Agent
from crewai import LLM
from tools import FinancialDocumentTool

load_dotenv()

# ==============================
# LLM Configuration
# ==============================


llm = LLM(
    model="openrouter/openai/gpt-3.5-turbo",
    api_base="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.2
)
# ==============================
# Financial Analyst Agent
# ==============================

financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal=(
        "Analyze the provided financial document and extract accurate financial "
        "information strictly based on document content. "
        "Answer the user's query using factual data from the document."
    ),
    backstory=(
        "You are a certified financial analyst with strong expertise in financial "
        "statement analysis, risk evaluation, and investment assessment. "
        "You do not speculate. You base all conclusions strictly on document data."
    ),
    verbose=True,
    memory=False,
    tools=[FinancialDocumentTool()],
    llm=llm,
    max_iter=1,
    allow_delegation=False
)
