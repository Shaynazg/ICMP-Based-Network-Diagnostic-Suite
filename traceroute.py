import socket
import struct
import time
import os
from ping import create_packet

def run_traceroute(target, max_hops=30):

    try:
        ip = socket.gethostbyname(target)

        result = f"Traceroute to {target} ({ip})\n\n"

        identifier = os.getpid() & 0xFFFF

        for ttl in range(1, max_hops + 1):

            sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_RAW,
                socket.IPPROTO_ICMP
            )

            sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
            sock.settimeout(2)

            packet = create_packet(identifier, ttl)

            start = time.time()
            sock.sendto(packet, (ip, 1))

            try:
                recv_packet, addr = sock.recvfrom(1024)
                end = time.time()

                rtt = (end - start) * 1000
                curr_addr = addr[0] #addr of router that just replied

                # getICMP type
                icmp_header = recv_packet[20:28]
                type_, _, _, _, _ = struct.unpack("!BBHHH", icmp_header)

                result += f"{ttl}\t{curr_addr}\t{rtt:.2f} ms\n"

                # if destination is reached
                if type_ == 0:
                    break

            except socket.timeout:
                result += f"{ttl}\t*\tRequest timed out\n"

            finally:
                sock.close()

        return result

    except Exception as e:
        return str(e)

