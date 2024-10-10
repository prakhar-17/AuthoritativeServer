from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

# In-memory storage for registered hostname and AS details
registered_info = {}

# Fibonacci function
def fibonacci(n):
    if n < 0:
        return "Invalid input"
    elif n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

# 1. Hostname Specification and Registration
@app.route('/register', methods=['PUT'])
def register():
    data = request.get_json()
    hostname = data.get("hostname")
    ip_address = data.get("ip")
    as_ip = data.get("as_ip")
    as_port = data.get("as_port")

    if not all([hostname, ip_address, as_ip, as_port]):
        return jsonify({"error": "Missing parameters"}), 400

    # Register with Authoritative Server (AS)
    dns_message = f"TYPE=A\nNAME={hostname}\nVALUE={ip_address}\nTTL=10\n"
    
    # Sending DNS message via UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(dns_message.encode(), (as_ip, int(as_port)))

    # Listen for confirmation from AS (optional, implement if necessary)
    # sock.settimeout(2)  # Set a timeout for receiving response
    try:
        response, _ = sock.recvfrom(4096)
        print("Received response from AS:", response.decode())
    except socket.timeout:
        return jsonify({"error": "Registration to AS failed"}), 500

    # Store registered info (if needed)
    registered_info[hostname] = {
        "ip": ip_address,
        "as_ip": as_ip,
        "as_port": as_port
    }

    return jsonify({"message": "Registered successfully"}), 201

# 2. Fibonacci Calculation
@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    number = request.args.get('number')

    # Validate the input
    try:
        number = int(number)
    except (ValueError, TypeError):
        return jsonify({"error": "Bad format"}), 400

    result = fibonacci(number)
    return jsonify({"fibonacci": result}), 200

if __name__ == '__main__':
    app.run(port=9090)
