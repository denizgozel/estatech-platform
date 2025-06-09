#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  8 17:32:05 2025

@author: denizgozel
"""

# dashboard_streamlit.py - Streamlit-based frontend for Estatech.ch platform

import streamlit as st
from main import property_db
from ai_service import generate_property_description
from valuation_service import get_avm
from report_service import generate_report
import json

with open("property_db.json", "r") as f:
    property_db = json.load(f)
property_db = {int(k): v for k, v in property_db.items()}

st.set_page_config(page_title="Estatech.ch Dashboard", layout="wide")
st.title("🏡 Estatech.ch | Luxury Property Intelligence Dashboard")

selected_id = st.selectbox("Select Property ID", list(property_db.keys()))
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
    avm = get_avm(prop["address"])
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
