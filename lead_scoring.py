#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  8 17:32:48 2025

@author: denizgozel
"""

# lead_scoring.py - Client profiling and lead scoring system

from typing import Dict
import math


def score_lead(lead_features: Dict) -> Dict:
    """
    Compute a score (0–100) indicating how hot a lead is based on behavior and demographics.
    Input: lead_features = {
        "income": int,
        "search_duration_months": int,
        "property_interactions": int,
        "clicked_ads": int
    }
    """
    income = lead_features.get("income", 0)
    duration = lead_features.get("search_duration_months", 0)
    interactions = lead_features.get("property_interactions", 0)
    clicks = lead_features.get("clicked_ads", 0)

    # Normalized sub-scores
    income_score = min(income / 1_000_000, 1.0) * 30
    urgency_score = max(1 - (duration / 12), 0) * 20
    interest_score = min(interactions / 20, 1.0) * 30
    engagement_score = min(clicks / 5, 1.0) * 20

    total_score = income_score + urgency_score + interest_score + engagement_score
    level = "Cold"
    if total_score > 75:
        level = "Hot"
    elif total_score > 50:
        level = "Warm"

    return {
        "score": round(total_score, 1),
        "level": level,
        "income_score": round(income_score, 1),
        "urgency_score": round(urgency_score, 1),
        "interest_score": round(interest_score, 1),
        "engagement_score": round(engagement_score, 1)
    }


# Example usage:
if __name__ == "__main__":
    example = {
        "income": 450_000,
        "search_duration_months": 4,
        "property_interactions": 15,
        "clicked_ads": 3
    }
    print(score_lead(example))