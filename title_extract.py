# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 19:09:40 2025

@author: Home-v3
"""

import json

CACHE_FILE = "anime_cache_full.json"        # your big scraped file
OUTPUT_JSON = "titles.json"         # list form for JS

def load_cache(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
def extract_english_titles(data):
    entries = []
    for item in data:
        title = item.get("title_english") or item.get("title")
        if title and isinstance(title, str):
            clean = title.strip()
            if clean:
                entries.append({
                    "title": clean,
                    "popularity": item.get("popularity"),
                    "members": item.get("members")
                })
    return entries

def save_files(titles):
    # Line-by-line text for feeding the Markov model

    # JSON list (optional for frontend)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(titles, f, ensure_ascii=False, indent=2)

def main():
    data = load_cache(CACHE_FILE)
    titles = extract_english_titles(data)
    print(f"Extracted {len(titles)} clean titles.")

    save_files(titles)
    print(f"Saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
