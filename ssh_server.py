import os
import paramiko
import socket
import sys
import threading

CWD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, "test_rsa.key"))

class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, channel_id):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_auth_password(self, username, password):
        if (username == "kali") and (password == "kali"):
            return paramiko.AUTH_SUCCESSFUL
        
def main():
    server_address = os.environ.get("IP") or "127.0.0.1"
    port = 2222
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server_address, port))
        sock.listen(100)
        print(f"[+] Listening for connection on {server_address}:{port} ...")
        client, addr = sock.accept()
    except Exception as e:
        print(f"[-] Listen failed: {str(e)}")
        sys.exit(1)
    else:
        print(f"[+] Got a connection. Socket info: {client} Client address: {addr}")
    
    session = paramiko.Transport(client)
    session.add_server_key(HOSTKEY)
    server = Server()
    session.start_server(server=server)

    channel = session.accept(30)
    if channel is None:
        print("[!] No channel.")
        sys.exit(1)
    
    print("[+] Authenticated!")
    print(channel.recv(1024).decode())
    channel.send("Welcome to SSH")
    try:
        while True:
            command = input("Enter command: ")
            if command == "exit":
                channel.send("exit")
                print("Exiting")
                session.close()
                # client.close()
                break
            else:
                channel.send(command)
                response = channel.recv(4096)
                print(response.decode())
    except KeyboardInterrupt:
        session.close()
        # client.close()

if __name__ == "__main__":
    main()