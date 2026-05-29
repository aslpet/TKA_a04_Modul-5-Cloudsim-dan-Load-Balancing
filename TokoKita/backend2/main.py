"""Backend Server 2 for TokoKita e-commerce application."""

import socket
from flask import Flask, jsonify

app = Flask(__name__)

# Hardcoded product catalog data (same as Server 1)
PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 12000000},
    {"id": 2, "name": "Mouse", "price": 150000},
    {"id": 3, "name": "Keyboard", "price": 350000}
]


@app.route("/")
def index():
    """Return server identity with hostname."""
    hostname = socket.gethostname()
    return jsonify({
        "server": "Server 2 - TokoKita",
        "hostname": hostname
    })


@app.route("/products")
def products():
    """Return the product catalog."""
    return jsonify(PRODUCTS)


if __name__ == "__main__":
    # NOTE: 0.0.0.0 is required inside Docker containers for inter-container
    # communication. This is NOT exposed directly to the public internet;
    # NGINX acts as the reverse proxy in front.
    # TODO(security): In production, use a proper WSGI server (e.g., gunicorn)
    # instead of Flask's built-in development server.
    app.run(host="0.0.0.0", port=5000)
