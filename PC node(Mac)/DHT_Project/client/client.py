import socket
import json

def send_request(node_ip, node_port, command):
    """Send a request to a specific node."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((node_ip, node_port))
            client_socket.send(json.dumps(command).encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
        return response
    except Exception as e:
        return f"Error connecting to {node_ip}:{node_port} - {str(e)}"

if __name__ == "__main__":
    # Load nodes configuration
    with open("nodes_config.json", "r") as file:
        nodes = json.load(file)

    print("Available nodes:")
    for i, node in enumerate(nodes):
        print(f"{i + 1}. {node['ip']}:{node['port']}")

    node_choice = int(input("Choose a node to connect to: ")) - 1
    node_ip = nodes[node_choice]['ip']
    node_port = nodes[node_choice]['port']

    while True:
        print("\nOptions:")
        print("1. Store Key-Value")
        print("2. Retrieve Key")
        print("3. Show All Keys")
        print("4. Exit")
        choice = int(input("Enter choice: "))

        if choice == 1:
            key = input("Enter key: ")
            value = input("Enter value: ")
            command = {"type": "store", "key": key, "value": value}
            print(send_request(node_ip, node_port, command))

        elif choice == 2:
            key = input("Enter key: ")
            command = {"type": "retrieve", "key": key}
            print(send_request(node_ip, node_port, command))

        elif choice == 3:
            command = {"type": "show_all"}
            print(send_request(node_ip, node_port, command))

        elif choice == 4:
            break

        else:
            print("Invalid choice. Try again.")
