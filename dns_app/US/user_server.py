# user_server.py

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    # Step 1: Query the Authoritative Server (AS) to resolve the hostname to IP
    as_url = f"http://{as_ip}:{as_port}/resolve?hostname={hostname}"
    response = requests.get(as_url)

    if response.status_code == 200:
        # Step 2: Get the IP of the Fibonacci Server (FS) from AS response
        fs_ip = response.json()['ip']

        # Step 3: Query FS for the Fibonacci number
        fs_url = f"http://{fs_ip}:{fs_port}/fibonacci?number={number}"
        fib_response = requests.get(fs_url)

        if fib_response.status_code == 200:
            fib_value = fib_response.json()['fibonacci']
            return jsonify({"fibonacci": fib_value}), 200
        else:
            return jsonify({"error": "Failed to get Fibonacci number"}), 500
    else:
        return jsonify({"error": "Failed to resolve hostname"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
