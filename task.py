# task.py

from crewai import Task
from agents import financial_analyst

analyze_financial_document = Task(
    description="""
    Analyze the following financial document content:

    {document_content}

    Extract:
    - Revenue
    - Expenses
    - Net Profit
    - Liabilities
    - Assets
    - Debt
    - Risk Indicators

    Answer the user's query: {query}

    Provide structured JSON output.
    Base your response strictly on the provided content.
    Do not fabricate information.
    """,

    expected_output="""
    Provide output in JSON format:

    {
        "revenue": "",
        "expenses": "",
        "net_profit": "",
        "liabilities": "",
        "assets": "",
        "debt": "",
        "risk_analysis": "",
        "investment_summary": ""
    }
    """,

    agent=financial_analyst,
    async_execution=False,
)