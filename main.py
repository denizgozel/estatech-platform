#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  8 17:28:40 2025
@author: denizgozel
"""

from fastapi import FastAPI
from fastapi.responses import Response, HTMLResponse
from typing import Dict
import json
import os

from ai_service import generate_property_description
from valuation_service import get_avm
from report_service import generate_report

app = FastAPI()

# ✅ Load property DB from JSON file
PROPERTY_DB_PATH = "property_db.json"

def load_property_db() -> Dict[int, Dict]:
    with open(PROPERTY_DB_PATH, "r") as f:
        data = json.load(f)
    # Ensure keys are integers (JSON keys are strings by default)
    return {int(k): v for k, v in data.items()}

property_db = load_property_db()

@app.get("/")
def root():
    return HTMLResponse("""
    <html><body>
    <h1>Estatech.ch AI Luxury Real Estate Platform</h1>
    <ul>
      <li><a href="/generate-description/1">Generate AI Description</a></li>
      <li><a href="/valuation/1">Get AVM</a></li>
      <li><a href="/download-report/1">Download PDF Report</a></li>
    </ul>
    </body></html>
    """)

@app.get("/generate-description/{prop_id}")
def gen_desc(prop_id: int):
    features = property_db[prop_id]["features"]
    description = generate_property_description(features)
    return {"description": description}

@app.get("/valuation/{prop_id}")
def get_valuation(prop_id: int):
    address = property_db[prop_id]["address"]
    return get_avm(address)

@app.get("/download-report/{prop_id}")
def download_report(prop_id: int):
    prop = property_db[prop_id]
    pdf = generate_report(prop)
    return Response(content=pdf, media_type="application/pdf")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("estatech_main:app", host="0.0.0.0", port=8000, reload=True)
