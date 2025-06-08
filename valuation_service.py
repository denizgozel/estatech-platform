#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  8 17:30:30 2025

@author: denizgozel
"""

# valuation_service.py - Simulates or connects to real estate market valuation APIs

import random
import datetime

def get_avm(address: str) -> dict:
    """
    Simulates an automated valuation model (AVM) response. Replace with real API integration if needed.
    """
    # Simulated data (in CHF)
    base_value = random.randint(2_000_000, 5_000_000)
    confidence = round(random.uniform(0.85, 0.98), 2)

    # Generate sample neighborhood trend data
    trends = [
        {"month": (datetime.date.today().replace(day=1) - datetime.timedelta(days=30*i)).strftime("%b %Y"),
         "price": int(base_value * (1 + random.uniform(-0.03, 0.04)))
        }
        for i in reversed(range(6))
    ]

    return {
        "estimated_value": base_value,
        "confidence": confidence,
        "neighborhood_trends": trends,
        "currency": "CHF",
        "address": address
    }
