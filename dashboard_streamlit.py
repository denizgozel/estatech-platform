#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  8 17:32:05 2025

@author: denizgozel
"""

# dashboard_streamlit.py - Streamlit-based frontend for Estatech.ch platform

import streamlit as st
import json
import os
from ai_service import generate_property_description
from valuation_service import get_avm
from report_service import generate_report

DB_FILE = "property_db.json"

# Load property DB from JSON
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        property_db = json.load(f)
        property_db = {int(k): v for k, v in property_db.items()}
else:
    property_db = {}

st.set_page_config(page_title="Estatech.ch Dashboard", layout="wide")
st.title("🏡 Estatech.ch | Luxury Property Intelligence Dashboard")

# Select existing property
selected_id = st.selectbox("Select Property ID", list(property_db.keys()))
if selected_id:
    prop = property_db[selected_id]

    st.header(prop["title"])
    st.subheader("📍 " + prop["features"]["location"])

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Features")
        st.write(f"- Size: {prop['features']['area']}")
        st.write(f"- Bedrooms: {prop['features']['bedrooms']}")
        st.write(f"- Bathrooms: {prop['features']['bathrooms']}")
        st.write(f"- Special: {', '.join(prop['features']['special_features'])}")

    with col2:
        st.write("### Market Valuation")
        if "valuation" not in prop:
            prop["valuation"] = get_avm(prop["address"])
            property_db[selected_id] = prop
            with open(DB_FILE, "w") as f:
                json.dump({str(k): v for k, v in property_db.items()}, f, indent=2)

        avm = prop["valuation"]
        st.metric("Estimated Value", f"CHF {avm['estimated_value']:,}")
        st.progress(avm['confidence'])
        st.line_chart({entry['month']: entry['price'] for entry in avm['neighborhood_trends']})

    st.divider()

    if st.button("📝 Generate AI Description"):
        desc = generate_property_description(prop["features"])
        st.success("Generated Description:")
        st.write(desc)

    if st.button("📄 Download PDF Report"):
        pdf_bytes = generate_report(prop)
        st.download_button("Download PDF", pdf_bytes, file_name="estatech_report.pdf", mime="application/pdf")

    if st.button("🗑️ Delete This Property"):
        del property_db[selected_id]
        with open(DB_FILE, "w") as f:
            json.dump({str(k): v for k, v in property_db.items()}, f, indent=2)
        st.experimental_rerun()

st.divider()


st.subheader("➕ Add a New Property")
with st.form("new_property_form"):
    new_id = st.number_input("Unique Property ID", min_value=1, step=1)
    title = st.text_input("Property Title")
    location = st.text_input("Location")
    area = st.text_input("Area (e.g., 300 sqm)")
    bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10)
    bathrooms = st.number_input("Bathrooms", min_value=1, max_value=10)
    special_features = st.text_area("Special Features (comma-separated)")
    address = st.text_input("Full Address")
    submitted = st.form_submit_button("Add Property")

    if submitted:
        if not title or not location or not address:
            st.error("Please fill in all required fields.")
        elif new_id in property_db:
            st.error(f"Property ID {new_id} already exists. Choose a different ID.")
        else:
            property_db[int(new_id)] = {
                "title": title,
                "features": {
                    "location": location,
                    "area": area,
                    "bedrooms": int(bedrooms),
                    "bathrooms": int(bathrooms),
                    "special_features": [s.strip() for s in special_features.split(",") if s.strip()]
                },
                "address": address,
                "lead_features": {
                    "income": 0,
                    "search_duration_months": 0,
                    "property_interactions": 0,
                    "clicked_ads": 0
                }
            }
            with open(DB_FILE, "w") as f:
                json.dump({str(k): v for k, v in property_db.items()}, f, indent=2)
            st.success(f"Property '{title}' added with ID {new_id}")
            st.experimental_rerun()

            with open(DB_FILE, "w") as f:
                json.dump({str(k): v for k, v in property_db.items()}, f, indent=2)
            st.success(f"Property '{title}' added with ID {new_id}")
            st.experimental_rerun()

# Save DB changes
if property_db:
    with open(DB_FILE, "w") as f:
        json.dump({str(k): v for k, v in property_db.items()}, f, indent=2)
