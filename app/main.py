from fastapi import FastAPI, UploadFile, File
from app.pdf_extract import extract_provider_report

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
