# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 13:42:41 2025

@author: Home-v3
"""

from flask import Flask, jsonify, render_template
import markovify, json

MODEL_FILE = "markov_model.json"

app = Flask(__name__)

# Load model
with open(MODEL_FILE, "r", encoding="utf-8") as f:
    model_json = json.load(f)
model = markovify.Text.from_json(json.dumps(model_json))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate")
def generate():
    title = None
    for _ in range(10):
        candidate = model.make_sentence(max_chars=80, tries=20)
        if candidate:
            title = candidate
            break
    if not title:
        title = "Untitled Project"
    return jsonify({"title": title})

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
