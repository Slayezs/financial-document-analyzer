from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid

from crewai import Crew, Process
from pypdf import PdfReader

from agents import financial_analyst
from task import analyze_financial_document as financial_task

app = FastAPI(title="Financial Document Analyzer")


# ==========================================
# PDF TEXT EXTRACTION
# ==========================================

def extract_pdf_text(file_path: str) -> str:
    try:
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

        return text.strip()

    except Exception as e:
        raise Exception(f"PDF extraction failed: {str(e)}")


# ==========================================
# CREW RUNNER
# ==========================================

def run_crew(query: str, file_path: str):
    # Extract PDF text
    document_content = extract_pdf_text(file_path)

    # 🔥 Prevent token overflow
    MAX_CHARS = 12000  # Safe limit for 16k token models

    if len(document_content) > MAX_CHARS:
        document_content = (
            document_content[:6000]
            + "\n\n...[CONTENT TRUNCATED FOR TOKEN LIMIT]...\n\n"
            + document_content[-6000:]
        )

    financial_crew = Crew(
        agents=[financial_analyst],
        tasks=[financial_task],
        process=Process.sequential,
    )

    result = financial_crew.kickoff({
        "query": query,
        "document_content": document_content
    })

    return result


# ==========================================
# ROUTES
# ==========================================

@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}


@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):

    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"

    try:
        os.makedirs("data", exist_ok=True)

        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        if not query:
            query = "Analyze this financial document for investment insights"

        response = run_crew(
            query=query.strip(),
            file_path=file_path
        )

        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing financial document: {str(e)}"
        )

    finally:
        # Cleanup
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)