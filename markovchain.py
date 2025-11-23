# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 13:35:42 2025

@author: Home-v3
"""

import json
import markovify

INPUT_JSON = r"C:\Users\rahul\Documents\anime_gen_py\anime_cache_full.json"
OUTPUT_MODEL = "markov_model.json"

def main():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Adapt to your structure
    titles = [item["title_english"] for item in data if item.get("title_english")]

    # Combine into one big text block
    text = "\n".join(titles)

    # Build Markov model
    model = markovify.NewlineText(text, state_size=2)

    # Export to JSON
    model_json = model.to_json()

    with open(OUTPUT_MODEL, "w", encoding="utf-8") as f:
        f.write(model_json)

    print("Saved model.")

if __name__ == "__main__":
    main()
