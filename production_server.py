#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  8 17:35:59 2025

@author: denizgozel
"""

# production_server.py - WSGI-compatible entrypoint for Estatech.ch production deployment

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from typing import List
import os

from ai_service import generate_property_description
from valuation_service import get_avm
from report_service import generate_report
from lead_scoring import score_lead
from media_integration import save_media_files, list_media
from marketing_generator import generate_social_post

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Estatech.ch AI Platform", docs_url="/docs")

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
      <head><title>Estatech AI Platform</title></head>
      <body>
        <h1>🏡 Estatech.ch - AI-Powered Luxury Real Estate Platform</h1>
        <ul>
          <li><a href="/generate-description/1">Generate Description</a></li>
          <li><a href="/valuation/1">Get Valuation</a></li>
          <li><a href="/download-report/1">Download Report</a></li>
        </ul>
      </body>
    </html>
    """


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory data
property_db = {
    1: {
        "title": "Lakeside Villa with Infinity Pool",
        "features": {
            "location": "Montreux, Switzerland",
            "area": "450 sqm",
            "bedrooms": 5,
            "bathrooms": 4,
            "special_features": ["Infinity pool", "Lake view", "Private dock"],
        },
        "address": "Chemin de la Tour 12, Montreux, Switzerland",
        "lead_features": {
            "income": 500000,
            "search_duration_months": 4,
            "property_interactions": 15,
            "clicked_ads": 3
        }
    }
}

@app.get("/description/{prop_id}")
def description(prop_id: int):
    features = property_db[prop_id]["features"]
    return {"description": generate_property_description(features)}

@app.get("/valuation/{prop_id}")
def valuation(prop_id: int):
    return get_avm(property_db[prop_id]["address"])

@app.get("/report/{prop_id}")
def report(prop_id: int):
    pdf_bytes = generate_report(property_db[prop_id])
    pdf_path = f"report_{prop_id}.pdf"
    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes)
    return FileResponse(pdf_path, media_type="application/pdf", filename=pdf_path)

@app.get("/lead_score/{prop_id}")
def lead_score(prop_id: int):
    return score_lead(property_db[prop_id]["lead_features"])

@app.post("/upload_media/{prop_id}")
def upload_media(prop_id: int, files: List[UploadFile] = File(...)):
    paths = save_media_files(prop_id, files)
    return {"saved_files": paths}

@app.get("/list_media/{prop_id}")
def list_uploaded_media(prop_id: int):
    return {"media_files": list_media(prop_id)}

@app.get("/generate_post/{prop_id}")
def marketing_post(prop_id: int):
    prop = property_db[prop_id]
    return {"post": generate_social_post(
        prop["title"],
        prop["features"]["location"],
        prop["features"]["special_features"]
    )}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("production_server:app", host="0.0.0.0", port=8000, reload=False)