# -*- coding: utf-8 -*-
"""
Scrape up to 1000 pages of anime data from Jikan API (v4)
Stores:
- title
- title_english
- genres
- themes
- demographic
- type
- year
-popularity
"""

import requests
import time
import json
import sys

API_BASE = "https://api.jikan.moe/v4/anime"
REQUEST_INTERVAL = 0.45  # stay polite to Jikan
CACHE_FILE = "anime_cache_full.json2"


def fetch_page(params, page):
    params = dict(params)
    params["page"] = page

    try:
        resp = requests.get(API_BASE, params=params, timeout=15)
        if resp.status_code == 200:
            return resp.json()
        else:
            print(f"HTTP {resp.status_code} on page {page}", file=sys.stderr)
            return None
    except requests.RequestException as e:
        print(f"Request failed: {e}", file=sys.stderr)
        return None


def extract_item(item):
    """Extract only the fields we actually care about."""
    title = item.get("title")
    title_eng = item.get("title_english")

    # genres, themes, demographics are lists of objects
    genres = [g["name"] for g in (item.get("genres") or [])]
    themes = [t["name"] for t in (item.get("themes") or [])]
    demos = [d["name"] for d in (item.get("demographics") or [])]

    # type (TV, Movie, OVA...)
    anime_type = item.get("type")

    # year might be None
    year = item.get("year")
    
    # ✅ popularity info we want for difficulty
    popularity = item.get("popularity")
    rank = item.get("rank")
    members = item.get("members")     # rough measure of visibility
    score = item.get("score") 

    return {
        "title": title or None,
        "title_english": title_eng or None,
        "genres": genres,
        "themes": themes,
        "demographic": demos[0] if demos else None,
        "type": anime_type,
        "year": year,
        "popularity": popularity,
        "rank": rank,
        "members": members,
        "score": score
    }


def gather_anime(max_pages=1000, limit=25, extra_params=None):
    if extra_params is None:
        extra_params = {}

    params = {"limit": limit}
    params.update(extra_params)

    results = []
    page = 1
    start = time.time()

    while page <= max_pages:
        data = fetch_page(params, page)
        if not data:
            print(f"Stopping at page {page} due to fetch failure.")
            break

        items = data.get("data", [])
        if not items:
            print(f"No items at page {page}. Stopping.")
            break

        # Extract useful info
        for item in items:
            results.append(extract_item(item))

        elapsed = time.time() - start
        print(f"✅ Page {page}/{max_pages} — Total entries: {len(results)} — {elapsed:.1f}s elapsed")

        # Save progress every 10 pages
        if page % 10 == 0:
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"💾 Progress saved. ({len(results)} items)")

        # Stop if no next page
        if not data.get("pagination", {}).get("has_next_page", False):
            print("🚩 No more pages.")
            break

        page += 1
        time.sleep(REQUEST_INTERVAL)

    # Final save
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 Done! Saved {len(results)} anime entries to {CACHE_FILE}.")

    return results


if __name__ == "__main__":
    gather_anime(max_pages=1000, limit=25)
