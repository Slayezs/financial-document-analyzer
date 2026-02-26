from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base


class FinancialAnalysis(Base):
    __tablename__ = "financial_analyses"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    query = Column(Text, nullable=False)
    analysis_result = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())