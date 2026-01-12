from fastapi import FastAPI, UploadFile, File
from app.pdf_extract import extract_text

import tempfile
import json

app = FastAPI(title="PDF API")


@app.post("/extract/text")
async def extract_pdf_text(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    text = extract_text(tmp_path)

    return {
        "filename": file.filename,
        "n_characters": len(text),
        "preview": text[:500]
    }
