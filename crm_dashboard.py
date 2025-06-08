#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  8 17:34:53 2025

@author: denizgozel
"""

# crm_dashboard.py - CRM and analytics dashboard logic for Estatech.ch

import pandas as pd
import streamlit as st
from lead_scoring import score_lead
from estatech_main import property_db

st.set_page_config(page_title="Estatech CRM", layout="wide")
st.title("📊 Estatech.ch | CRM & Lead Intelligence")

# Simulated client data for demonstration
clients = [
    {"name": "Anna Keller", "prop_id": 1, "lead_features": {
        "income": 450000,
        "search_duration_months": 4,
        "property_interactions": 15,
        "clicked_ads": 3
    }},
    {"name": "Luca Moretti", "prop_id": 1, "lead_features": {
        "income": 700000,
        "search_duration_months": 2,
        "property_interactions": 20,
        "clicked_ads": 4
    }},
    {"name": "Sophie Dubois", "prop_id": 1, "lead_features": {
        "income": 300000,
        "search_duration_months": 8,
        "property_interactions": 7,
        "clicked_ads": 1
    }}
]

rows = []
for client in clients:
    score_data = score_lead(client["lead_features"])
    rows.append({
        "Client": client["name"],
        "Property": property_db[client["prop_id"]]["title"],
        "Score": score_data["score"],
        "Level": score_data["level"],
        "Income Score": score_data["income_score"],
        "Urgency": score_data["urgency_score"],
        "Interest": score_data["interest_score"],
        "Engagement": score_data["engagement_score"]
    })

st.subheader("🔎 Lead Heatmap")
df = pd.DataFrame(rows)
st.dataframe(df.style.background_gradient(cmap="Oranges", subset=["Score"]))

st.bar_chart(df.set_index("Client")["Score"])
st.caption("Scores combine income, urgency, interest and engagement to classify lead quality.")