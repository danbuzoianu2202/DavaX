from flask import Flask, jsonify, request, abort
from datetime import datetime

app = Flask(__name__)

# In-memory store (for demo only)
ITEMS = {}
REQUEST_COUNTER = {"total": 0}


@app.before_request
def count_requests():
    REQUEST_COUNTER["total"] += 1


@app.get("/")
def home():
    return "Hello, World from a more capable Flask service"


@app.get("/health")
def health():
    return jsonify(status="ok", time=datetime.utcnow().isoformat() + "Z")


@app.get("/time")
def time_now():
    return jsonify(now=datetime.utcnow().isoformat() + "Z")


@app.get("/greet/<name>")
def greet(name):
    return jsonify(message=f"Hello, {name}")


@app.get("/echo")
def echo():
    msg = request.args.get("msg", "")
    return jsonify(echo=msg)


@app.post("/compute/sum")
def compute_sum():
    data = request.get_json(silent=True) or {}
    numbers = data.get("numbers")
    if not isinstance(numbers, list) or not all(isinstance(x, (int, float)) for x in numbers):
        abort(400, description="Provide JSON like {\"numbers\": [1,2,3]}")
    return jsonify(result=sum(numbers))


# CRUD-like demo for items
@app.post("/items")
def create_item():
    payload = request.get_json(silent=True) or {}
    if "id" not in payload or "name" not in payload:
        abort(400, description="Provide JSON with 'id' and 'name'")
    item_id = str(payload["id"])
    ITEMS[item_id] = {"id": item_id,
                      "name": payload["name"],
                      "created_at": datetime.utcnow().isoformat() + "Z"}
    return jsonify(ITEMS[item_id]), 201


@app.get("/items/<item_id>")
def read_item(item_id):
    item = ITEMS.get(str(item_id))
    if not item:
        abort(404, description="Item not found")
    return jsonify(item)


@app.delete("/items/<item_id>")
def delete_item(item_id):
    removed = ITEMS.pop(str(item_id), None)
    if not removed:
        abort(404, description="Item not found")
    return "", 204


@app.get("/metrics")
def metrics():
    # Minimal, human-readable metrics endpoint (not Prometheus format)
    return jsonify(requests=REQUEST_COUNTER["total"], items=len(ITEMS))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
