## Some Python networking tools

Note: it is recommended to use a Python virtual environment. The necessary packages and versions can be found in requirements.txt.

*venv* is a lightweight virtual environment module in the Python standard library that serves this purpose.

Example:
```
~/$ python3 -m venv my_venv
~/$ . my_venv/bin/activate
(my_venv) ~/$ pip install -r requirements.txt
```

### TCP Client/Server
*(tcp_client.py, tcp_server.py)*

A basic TCP client and server pair.

* Start the server: `python tcp_server.py -i 127.0.0.1 -p 9999`

Listening on port 9999 at the loopback address. Can use any valid IP address used by a network interface on the machine. Default is 0.0.0.0 (all addresses).

* Connect to the server: `python tcp_client.py -i 127.0.0.1 -p 9999`

Connects to the provided IP address at the provided port number.

Now communication can be sent from client to server. Exit via Ctrl-C.

### Netcat
*(netcat.py)*

A custom implementation of netcat, for more flexible reading and writing of data. Can be started in listener mode (i.e. server) or client mode. Has options to set up an interactive shell (-c), execute one specified command (-e), or upload a file (-u).

* First, set up a listener with the -l flag, specifying that we want to set up a shell:
`python netcat.py -t 192.168.1.32 -p 9999 -l -c`

* Then, connect and interact with the shell:
`python netcat.py -t 192.168.1.32 -p 9999`

* Or, set up a listener to execute a predetermined command when connected to, and send output to the client:
`python netcat.py -t 192.168.1.32 -p 9999 -l -e pwd`

* Or, set up a listener to write data received from the client to a file:
`python netcat.py -t 192.168.1.32 -p 9999 -l -u myfile`

### Proxy
*(proxy.py)*

A TCP proxy that forwards traffic between the specified local and remote targets.

* Usage: `python proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]`

* Example: `python proxy.py 192.168.1.32 21 ftp.sun.ac.za 21 true`

Note: if provided localport is a privileged port, may need to run with `sudo`.

`receive_first` specifies whether the proxy expects to receive data from remote (e.g. an FTP banner) before beginning to send local client data.

### Reverse SSH Client/Server
*(ssh_server.py, ssh_rcmd.py)*

A reverse SSH client and server that, after the client connects to the server, allows the server to run commands on the client. Uses the Paramiko library for implementation of the SSHv2 protocol.

Example:

**Server**
```
python ssh_server.py
Listening for connection...
```

**Client**
```
python ssh_rcmd.py
Username: kali
Password: 
Enter server IP: 192.168.1.44
Enter port: 22
Welcome to SSH
```

**Server**
```
[+] Got a connection. Socket info: <socket.socket fd=4, family=2, type=1, proto=0, laddr=('192.168.1.44', 22), raddr=('192.168.1.44', 41364)> Client address: ('192.168.1.44', 41364)
[+] Authenticated!
ClientConnected
Enter command:
```
