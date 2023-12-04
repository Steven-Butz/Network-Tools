import getpass
import paramiko
import shlex
import subprocess

def ssh_command(ip, port, user, passwd, cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip, port, user, passwd)
    except Exception as e:
        print(f"[!] Could not connect to {ip}:{port}")
        print(str(e))
        return

    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(cmd)
        print(ssh_session.recv(1024).decode())
        while True:
            command = ssh_session.recv(1024)
            try:
                cmd = command.decode()
                if cmd == "exit":
                    client.close()
                    break
                print(shlex.split(cmd))
                cmd_output = subprocess.check_output(shlex.split(cmd), shell=False)
                print(cmd_output)
                ssh_session.send(cmd_output or "okay")
            except Exception as e:
                ssh_session.send(str(e))
        client.close()
    return

if __name__ == "__main__":
    # user = getpass.getuser()
    user = input("Username: ")
    password = getpass.getpass()

    ip = input("Enter server IP: ")
    port = input("Enter port: ")
    ssh_command(ip, port, user, password, "ClientConnected")