#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  8 17:31:00 2025

@author: denizgozel
"""

# report_service.py - Generates PDF reports for luxury real estate listings

from weasyprint import HTML, CSS
from jinja2 import Template
from valuation_service import get_avm
from ai_service import generate_property_description
import tempfile

html_template = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: 'Helvetica Neue', sans-serif; color: #222; margin: 2em; }
        h1 { color: #1a1a1a; font-size: 28px; }
        h2 { font-size: 22px; color: #444; }
        .section { margin-bottom: 2em; }
        .features ul { list-style: none; padding: 0; }
        .features ul li { padding: 4px 0; }
        .trend-table { width: 100%; border-collapse: collapse; margin-top: 1em; }
        .trend-table th, .trend-table td { border: 1px solid #ccc; padding: 8px; text-align: left; }
    </style>
</head>
<body>
    <h1>{{ title }}</h1>
    <div class="section">
        <h2>Description</h2>
        <p>{{ description }}</p>
    </div>
    <div class="section features">
        <h2>Property Features</h2>
        <ul>
            <li><strong>Location:</strong> {{ features.location }}</li>
            <li><strong>Size:</strong> {{ features.area }}</li>
            <li><strong>Bedrooms:</strong> {{ features.bedrooms }}</li>
            <li><strong>Bathrooms:</strong> {{ features.bathrooms }}</li>
            <li><strong>Special:</strong> {{ features.special_features | join(", ") }}</li>
        </ul>
    </div>
    <div class="section">
        <h2>Estimated Market Value</h2>
        <p><strong>Address:</strong> {{ address }}</p>
        <p><strong>Estimated Value:</strong> CHF {{ valuation.estimated_value | string | replace(',', ' ') }}</p>
        <p><strong>Confidence:</strong> {{ valuation.confidence * 100 | round(1) }}%</p>
        <table class="trend-table">
            <thead><tr><th>Month</th><th>Estimated Price (CHF)</th></tr></thead>
            <tbody>
            {% for entry in valuation.neighborhood_trends %}
                <tr><td>{{ entry.month }}</td><td>{{ entry.price }}</td></tr>
            {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
""")

def generate_report(property_data: dict) -> bytes:
    """
    Generate a PDF report for a given property.
    """
    description = generate_property_description(property_data["features"])
    valuation = get_avm(property_data["address"])

    html_content = html_template.render(
        title=property_data["title"],
        features=property_data["features"],
        address=property_data["address"],
        valuation=valuation,
        description=description
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        HTML(string=html_content).write_pdf(temp_pdf.name)
        temp_pdf.seek(0)
        return temp_pdf.read()