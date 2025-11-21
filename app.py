from flask import Flask, render_template, request, jsonify
from time import perf_counter
import os

from db import get_db, ensure_db
from nlp.engine import ChatEngine

app = Flask(__name__)
engine = None

@app.before_first_request
def _init():
    global engine
    ensure_db()  # creates ./campus.db if missing and seeds it
    engine = ChatEngine()

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/chat")
def chat():
    t0 = perf_counter()
    user_text = request.json.get("message", "").strip()
    reply, state = engine.respond(user_text)
    dt = (perf_counter() - t0) * 1000.0
    print(f"[latency] {dt:.1f} ms  [state] {state}")
    return jsonify({"reply": reply, "state": state})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(debug=True, port=port)
