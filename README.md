# ICMP-Based-Network-Diagnostic-Suite
A client-server network diagnostic tool that implements Ping and Traceroute using raw ICMP sockets with support for multi-client communication and TLS encryption.

# 1.Key Features
- ICMP-based Ping implementation (RTT & packet loss)
- ICMP-based Traceroute implementation using TTL probing
- Multithreaded server (handles multiple clients)
- Multi-destination support
- Secure communication using TLS/SSL

## 2. Implementaion Details
### 2.1 Ping Implementation
The server creates and sends ICMP Echo Request packets and waits for ICMP Echo Reply.
- Measures RTT
- Computes packet loss statistics 

### 2.2 Traceroute Implementation
Traceroute makes use of TTL manipulation:
- Server sends multiple ICMP Echo Request packets with an increasing value of TTL each time.
- Each router encountered decrements the TTL value by 1.
- When TTL reaches 0, routers send ICMP Time Exceeded responses, allowing the server to identify intermediate routers along the path.
- The destination host responds with an ICMP Echo Reply

# 3.Usage Instructions
Requirements: linux environment, python, OpenSSL 

Generate TLS certificates:
```bash
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes
```
Run server:
(Run with sudo)
```bash
sudo python3 server.py
```
Run one or more clients in separate terminals:
```bash
python3 client.py
```
Now in client terminal, run:
``` bash
ping google.com github.com
```
<img width="485" height="213" alt="image" src="https://github.com/user-attachments/assets/515c2526-affd-4d0a-90eb-b84c57bd7ab4" />

or
```bash
traceroute google.com github.com
```
<img width="377" height="276" alt="image" src="https://github.com/user-attachments/assets/495ab009-8ed3-4d18-857c-ae50b38e7beb" />


