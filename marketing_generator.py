#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  8 17:33:28 2025

@author: denizgozel
"""

# marketing_generator.py - AI-powered marketing content creator for luxury real estate

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import os

# Set your OpenAI API key (or load from environment)


def generate_social_post(property_title: str, location: str, features: list, platform: str = "Instagram") -> str:
    """
    Generates a platform-optimized social media post for a luxury property.
    """
    hashtags = "#luxuryhomes #realestate #estatech #swissluxury #propertyinvestment"
    feature_list = ", ".join(features[:3])

    prompt = (
        f"Create a compelling {platform} post to market a luxury property called '{property_title}' in {location}.\n"
        f"Highlight unique features like {feature_list}.\nInclude engaging emojis, elegant language, and suitable hashtags."
    )

    try:
        response = client.chat.completions.create(model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=150)
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error generating marketing post: {str(e)}]"


# Example usage:
if __name__ == "__main__":
    post = generate_social_post(
        property_title="Lakeside Villa with Infinity Pool",
        location="Montreux, Switzerland",
        features=["Infinity pool", "Private dock", "Panoramic lake views"],
        platform="Instagram"
    )
    print(post)
