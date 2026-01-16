from fastapi import FastAPI, UploadFile, File
from app.pdf_extract import extract_provider_report
from app.mydb import save_provider_report
from app.mydb import fetch_all_tables

import tempfile
import json

app = FastAPI(title="PDF API")

@app.post("/extract/all")
async def extract_pdf(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    res = extract_provider_report(tmp_path)

    return res

@app.post("/save/all")
async def extract_pdf(file: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # 1. Extract structured data from PDF
    report = extract_provider_report(tmp_path)

    # 2. Save extracted data to DB
    report_id = save_provider_report(report)

    return {
        "status": "ok",
        "report_id": report_id,
        "provider": report["provider_name"]
    }

@app.get("/tables/all")
def get_all_tables():
    return fetch_all_tables()
