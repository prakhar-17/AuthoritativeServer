import socket
import os

# DNS record storage file
RECORDS_FILE = "dns_records.txt"

# Function to register DNS records
def register_dns_record(message):
    lines = message.strip().splitlines()
    record = {}
    for line in lines:
        key, value = line.split('=')
        record[key.strip()] = value.strip()
    
    with open(RECORDS_FILE, 'a') as f:
        f.write(f"{record['NAME']},{record['VALUE']},{record['TYPE']},{record['TTL']}\n")
    
    return "Registration successful"

# Function to respond to DNS queries
def query_dns_record(name):
    if not os.path.exists(RECORDS_FILE):
        return "No records found"
    
    with open(RECORDS_FILE, 'r') as f:
        for line in f:
            record = line.strip().split(',')
            if record[0] == name:  # Check for matching name
                return f"TYPE={record[2]}\nNAME={record[0]}\nVALUE={record[1]}\nTTL={record[3]}"
    
    return "Record not found"

# UDP server to handle registration and queries
def start_authoritative_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 53533))
    print("Authoritative Server running on port 53533")

    while True:
        message, client_address = server_socket.recvfrom(4096)
        message = message.decode('utf-8')

        if "TYPE=A" in message and "NAME=" in message:
            response = register_dns_record(message)
        else:
            name = message.split("NAME=")[1].strip()
            response = query_dns_record(name)

        server_socket.sendto(response.encode('utf-8'), client_address)

if __name__ == '__main__':
    start_authoritative_server()
