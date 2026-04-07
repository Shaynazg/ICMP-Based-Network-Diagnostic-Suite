import socket
import struct
import time
import os

def run_ping(target, count=4):

    try:
        ip = socket.gethostbyname(target)

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_RAW,
            socket.IPPROTO_ICMP
        )

        identifier = os.getpid() & 0xFFFF

        sent = 0
        received = 0
        rtts = []

        for seq in range(count):
            sent += 1

            rtt = send_ping(sock, ip, identifier, seq)

            if rtt is not None:
                received += 1
                rtts.append(rtt)

            time.sleep(1)

        loss = ((sent - received) / sent) * 100

        avg_rtt = sum(rtts) / len(rtts) if rtts else 0

        return f"""
PING {target} ({ip})

Packets: Sent = {sent}, Received = {received}, Lost = {sent - received}
Packet Loss = {loss:.2f}%

Average RTT = {avg_rtt:.2f} ms
"""

    except PermissionError:
        return "Run server with sudo"

    except Exception as e:
        return str(e)
    


def checksum(data):
    s = 0
    n = len(data)

    for i in range(0, n - 1, 2):
        s += (data[i] << 8) + data[i + 1]

    if n % 2:
        s += data[-1] << 8

    s = (s >> 16) + (s & 0xffff)
    s += (s >> 16)

    return ~s & 0xffff

def create_packet(identifier, sequence):

    ICMP_ECHO_REQUEST = 8
    code = 0
    checksum_value = 0

    header = struct.pack("!BBHHH",
                         ICMP_ECHO_REQUEST,
                         code,
                         checksum_value,
                         identifier,
                         sequence)

    data = struct.pack("d", time.time())

    checksum_value = checksum(header + data)

    header = struct.pack("!BBHHH",
                         ICMP_ECHO_REQUEST,
                         code,
                         checksum_value,
                         identifier,
                         sequence)

    return header + data

def send_ping(sock, ip, identifier, sequence):

    packet = create_packet(identifier, sequence)

    start = time.time()

    sock.sendto(packet, (ip, 1))

    sock.settimeout(1)

    try:
        while True:
            
            recv_packet, addr = sock.recvfrom(1024)
            
            end = time.time()

            # get ICMP header (skip IP hdr)
            icmp_header = recv_packet[20:28]

            type_, code, checksum_recv, recv_id, recv_seq = struct.unpack("!BBHHH", icmp_header)

            if type_ == 0 and recv_id == identifier:
                return (end - start) * 1000

    except socket.timeout:
        return None
    
