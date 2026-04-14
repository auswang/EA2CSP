import os
from datetime import datetime, timezone, timedelta
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from move_support_data import get_move_support

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB max request size

CLIENT_ID = os.environ.get("AZURE_CLIENT_ID", "")
TENANT_ID = os.environ.get("AZURE_TENANT_ID", "common")
AUSTIN_TENANT = os.environ.get("AUSTIN_TENANT", "")
BUILD_TIME = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")


@app.route("/")
def index():
    return render_template(
        "index.html",
        client_id=CLIENT_ID,
        tenant_id=TENANT_ID,
        austin_tenant=AUSTIN_TENANT,
        build_time=BUILD_TIME,
    )


@app.route("/api/check-move", methods=["POST"])
def check_move():
    """Check move support for a list of resource types."""
    data = request.get_json()
    resources = data.get("resources", [])
    results = []
    for res in resources:
        resource_type = res.get("type", "")
        move_rg, move_sub = get_move_support(resource_type)
        results.append({
            "name": res.get("name", ""),
            "type": resource_type,
            "location": res.get("location", ""),
            "resourceGroup": res.get("resourceGroup", ""),
            "moveResourceGroup": "Yes" if move_rg else ("No" if move_rg is not None else "Unknown"),
            "moveSubscription": "Yes" if move_sub else ("No" if move_sub is not None else "Unknown"),
        })
    results.sort(key=lambda x: (x["moveSubscription"] != "Yes", x["type"]))
    return jsonify({"resources": results, "total": len(results)})


@app.route("/health")
def health():
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
