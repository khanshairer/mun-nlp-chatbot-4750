from flask import Flask, render_template, request, jsonify
from time import perf_counter
import os

from db import ensure_db, suggest_prof_names
from nlp.engine import ChatEngine
from import_faculty_from_excel import main as import_faculty

app = Flask(__name__)

# ----- DB + data initialization -----
ensure_db()

try:
    # Import / refresh faculty data from Excel into campus.db
    import_faculty()
    print("✅ Faculty data imported from Excel.")
except Exception as e:
    # If something goes wrong, app still runs, but with a warning
    print(f"⚠️ Could not import faculty data from Excel: {e}")

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


@app.get("/suggest")
def suggest():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify([])
    names = suggest_prof_names(q, limit=7)
    return jsonify(names)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(debug=True, port=port)
