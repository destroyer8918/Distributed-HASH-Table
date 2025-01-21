import socket
import json
import random
import string

# Define node configuration
nodes_config = [
    {"ip": "10.0.1.200", "port": 5001},  # Linux Node
    {"ip": "10.0.1.205", "port": 5002},  # Mac Node
    {"ip": "10.0.1.216", "port": 5056},  # Android Node
]

def generate_random_keys(num_keys):
    """Generate a list of random keys."""
    return [''.join(random.choices(string.ascii_letters + string.digits, k=5)) for _ in range(num_keys)]

def send_key_to_node(node, key, value):
    """Send a key-value pair to a node."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((node['ip'], node['port']))
            command = {"type": "store", "key": key, "value": value}
            client_socket.send(json.dumps(command).encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Response from {node['ip']}:{node['port']} - {response}")
    except Exception as e:
        print(f"Error sending key '{key}' to {node['ip']}:{node['port']} - {str(e)}")

def distribute_keys(keys):
    """Distribute keys across nodes."""
    for key in keys:
        # Assign a random value to the key
        value = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        # Send the key to all nodes (let their hashing rules decide where to store)
        for node in nodes_config:
            send_key_to_node(node, key, value)

# Main script
if __name__ == "__main__":
    print("Starting key distribution...")
    num_keys = 100  # Adjust the number of keys if needed
    random_keys = generate_random_keys(num_keys)
    print("Generated keys:", random_keys)
    distribute_keys(random_keys)
    print("Key distribution complete.")

