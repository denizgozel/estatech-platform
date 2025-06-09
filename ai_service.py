#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  8 17:29:28 2025

@author: denizgozel
"""

# ai_service.py - AI module for generating luxury property descriptions (OpenAI SDK v1+)

import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_property_description(features: dict) -> str:
    """
    Generate a luxury real estate description using GPT-4 based on input features.
    """
    prompt = (
        "You are a luxury real estate copywriter. Write an emotionally captivating and high-end property "
        "description suitable for a website like estatech.ch. Highlight luxury features and evoke lifestyle imagery.\n"
        f"Location: {features.get('location')}\n"
        f"Size: {features.get('area')}\n"
        f"Bedrooms: {features.get('bedrooms')}\n"
        f"Bathrooms: {features.get('bathrooms')}\n"
        f"Special Features: {', '.join(features.get('special_features', []))}\n"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error generating description: {str(e)}]"
