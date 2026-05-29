"""Backend Server 1 for TokoKita e-commerce application."""

import socket
from flask import Flask, jsonify

app = Flask(__name__)

# Hardcoded product catalog data
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
        "server": "Server 1 - TokoKita",
        "hostname": hostname
    })


@app.route("/products")
def products():
    """Return the product catalog."""
    return jsonify(PRODUCTS)


# soal 3
@app.route("/catalogue", methods=["GET"])
def catalogue():
    """Ringan. Hanya mengembalikan JSON data produk."""
    return jsonify(PRODUCTS)

@app.route("/checkout", methods=["POST"])
def checkout():
    """Sangat Berat. Lakukan perulangan komputasi matematika kompleks."""
    primes = []
    for possiblePrime in range(2, 10000):
        is_prime = True
        for num in range(2, int(possiblePrime ** 0.5) + 1):
            if possiblePrime % num == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(possiblePrime)
            
    return jsonify({"status": "success", "message": "Checkout complete"})


if __name__ == "__main__":
    # NOTE: 0.0.0.0 is required inside Docker containers for inter-container
    # communication. This is NOT exposed directly to the public internet;
    # NGINX acts as the reverse proxy in front.
    # TODO(security): In production, use a proper WSGI server (e.g., gunicorn)
    # instead of Flask's built-in development server.
    app.run(host="0.0.0.0", port=5000)
