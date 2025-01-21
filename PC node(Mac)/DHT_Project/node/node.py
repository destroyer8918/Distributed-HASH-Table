import socket
import threading
import json
import hashlib
import os

# Local storage for key-value pairs
storage = {}

def save_data():
    """Save storage to a JSON file."""
    with open("storage.json", "w") as file:
        json.dump(storage, file)

def load_data():
    """Load storage from a JSON file."""
    if os.path.exists("storage.json"):
        with open("storage.json", "r") as file:
            return json.load(file)
    return {}

def load_known_nodes():
    """Load known nodes from a JSON file."""
    if os.path.exists("known_nodes.json"):
        with open("known_nodes.json", "r") as file:
            return json.load(file)
    return []

def should_store_key(key):
    """Mac Node: Store keys based on SHA-1 divisible by 3."""
    hash_value = hashlib.sha1(key.encode()).hexdigest()
    numeric_value = int(hash_value, 16)  # Convert to base-16 integer
    should_store = numeric_value % 3 == 0  # Check if divisible by 3
    print(f"Mac Node: Key: {key}, SHA-1 Hash: {hash_value}, Numeric Value: {numeric_value}, Should Store: {should_store}")
    return should_store



def forward_request(node_ip, node_port, command, visited_nodes):
    """Forward the request to another node."""
    try:
        # Add current node to visited nodes
        command['visited_nodes'] = visited_nodes

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as forward_socket:
            forward_socket.connect((node_ip, node_port))
            forward_socket.send(json.dumps(command).encode('utf-8'))
            response = forward_socket.recv(1024).decode('utf-8')
        return response
    except Exception as e:
        return f"Error forwarding request to {node_ip}:{node_port} - {str(e)}"


def handle_client(client_socket):
    """Handle incoming client requests."""
    try:
        request = client_socket.recv(1024).decode('utf-8')
        command = json.loads(request)

        # Check if this node has already been visited
        visited_nodes = command.get('visited_nodes', [])
        if socket.gethostbyname(socket.gethostname()) in visited_nodes:
            client_socket.send("Error: Request already processed by this node.".encode('utf-8'))
            return

        # Add this node to the visited nodes
        visited_nodes.append(socket.gethostbyname(socket.gethostname()))

        if command['type'] == 'store':
            key = command['key']
            value = command['value']
            if should_store_key(key):  # Node-specific logic
                storage[key] = value
                save_data()
                response = f"Key '{key}' stored successfully with value '{value}'"
            else:
                # Forward the request to other known nodes
                response = "Key not stored on any node."
                for node in known_nodes:
                    if node['ip'] not in visited_nodes:
                        response = forward_request(node['ip'], node['port'], command, visited_nodes)
                        if "stored successfully" in response:
                            break

        elif command['type'] == 'retrieve':
            key = command['key']
            value = storage.get(key, None)
            if value:
                response = f"Key '{key}' found with value '{value}'"
            else:
                # Forward the retrieve request to other known nodes
                response = "Key not found on any node."
                for node in known_nodes:
                    if node['ip'] not in visited_nodes:
                        response = forward_request(node['ip'], node['port'], command, visited_nodes)
                        if "found with value" in response:
                            break

        elif command['type'] == 'show_all':
            response = json.dumps(storage)

        else:
            response = "Unknown command"

        client_socket.send(response.encode('utf-8'))

    except Exception as e:
        print(f"Error handling client: {e}")
        client_socket.send(f"Error: {str(e)}".encode('utf-8'))
    finally:
        client_socket.close()


def start_server(port):
    """Start the server to listen for incoming connections."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"Node started on port {port}. Waiting for connections...")
    
    while True:
        client_socket, addr = server.accept()
        print(f"Connection received from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    # Load storage and known nodes
    storage = load_data()
    known_nodes = load_known_nodes()
    
    port = int(input("Enter port number for this node: "))
    start_server(port)
