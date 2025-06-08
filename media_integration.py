#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  8 17:34:08 2025

@author: denizgozel
"""

# media_integration.py - Handles drone footage and media upload for property listings

import os
from fastapi import UploadFile
from typing import List

MEDIA_DIR = "media_uploads"
os.makedirs(MEDIA_DIR, exist_ok=True)


def save_media_files(property_id: int, files: List[UploadFile]) -> List[str]:
    """
    Saves uploaded media files to a structured directory.
    Returns a list of saved file paths.
    """
    prop_dir = os.path.join(MEDIA_DIR, f"property_{property_id}")
    os.makedirs(prop_dir, exist_ok=True)

    saved_paths = []
    for file in files:
        extension = os.path.splitext(file.filename)[-1].lower()
        filename = file.filename.replace(" ", "_")
        path = os.path.join(prop_dir, filename)
        with open(path, "wb") as f:
            f.write(file.file.read())
        saved_paths.append(path)

    return saved_paths


def list_media(property_id: int) -> List[str]:
    """
    Lists all saved media paths for a given property.
    """
    prop_dir = os.path.join(MEDIA_DIR, f"property_{property_id}")
    if not os.path.exists(prop_dir):
        return []
    return [os.path.join(prop_dir, f) for f in os.listdir(prop_dir)]


# Example usage:
if __name__ == "__main__":
    print("📸 Media directory is ready at:", MEDIA_DIR)
