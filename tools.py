import os
from dotenv import load_dotenv
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from pypdf import PdfReader

load_dotenv()


# ==========================================
# 📄 Financial Document Reader Tool
# ==========================================

class FinancialDocumentInput(BaseModel):
    file_path: str = Field(
        ...,
        description="Path to the uploaded financial document file"
    )


class FinancialDocumentTool(BaseTool):
    name: str = "Financial Document Reader"
    description: str = (
        "Reads and extracts text content from financial documents "
        "including PDF and TXT files."
    )

    args_schema: Type[BaseModel] = FinancialDocumentInput

    def _run(self, file_path: str) -> str:
        """
        Reads a financial document and extracts text.
        Supports PDF and TXT files.
        """

        try:
            if not os.path.exists(file_path):
                return f"Error: File not found at path {file_path}"

            # ======================
            # 📑 Handle PDF Files
            # ======================
            if file_path.lower().endswith(".pdf"):
                reader = PdfReader(file_path)
                text = ""

                for page in reader.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:
                        text += extracted_text + "\n"

                cleaned_text = text.strip()
                if not cleaned_text:
                    return "Warning: PDF text extraction returned empty content."

                return cleaned_text

            # ======================
            # 📄 Handle Text Files
            # ======================
            else:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                content = content.strip()
                content = "\n".join(line.strip() for line in content.splitlines())

                return content

        except Exception as e:
            return f"Error while reading document: {str(e)}"


# ==========================================
# 📊 Investment Analysis Tool
# ==========================================

class InvestmentInput(BaseModel):
    financial_document_data: str = Field(
        ...,
        description="Extracted financial document content for investment analysis"
    )


class InvestmentTool(BaseTool):
    name: str = "Investment Analysis Tool"
    description: str = (
        "Analyzes financial document data and generates structured investment insights."
    )

    args_schema: Type[BaseModel] = InvestmentInput

    def _run(self, financial_document_data: str) -> str:
        return "Investment analysis module to be implemented."


# ==========================================
# ⚠️ Risk Assessment Tool
# ==========================================

class RiskInput(BaseModel):
    financial_document_data: str = Field(
        ...,
        description="Extracted financial document content for risk assessment"
    )


class RiskTool(BaseTool):
    name: str = "Risk Assessment Tool"
    description: str = (
        "Performs structured risk analysis based on financial document data."
    )

    args_schema: Type[BaseModel] = RiskInput

    def _run(self, financial_document_data: str) -> str:
        return "Risk assessment module to be implemented."