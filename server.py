import socket
import sqlite3

# Define the DNS server's IP address and port
DNS_SERVER_IP = '10.10.10.1'
DNS_SERVER_PORT = 12345

# Create a connection to the DNS database
conn = sqlite3.connect('dns.db')
cursor = conn.cursor()

# Create the DNS table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS dns
                (domain text PRIMARY KEY, ip_address text)''')
conn.commit()

print('DNS server listening on {}:{}'.format(DNS_SERVER_IP, DNS_SERVER_PORT))

# Create a UDP socket and bind it to the DNS server's IP address and port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((DNS_SERVER_IP, DNS_SERVER_PORT))

while True:
    try:
        # Receive a DNS query packet from a client
        data, addr = sock.recvfrom(1024)

        # Decode the DNS query packet
        domain = data.decode().strip()

        # Look up the IP address for the requested domain in the DNS database
        cursor.execute("SELECT ip_address FROM dns WHERE domain=?", (domain,))
        result = cursor.fetchone()
        if result:
            ip_address = result[0]
        else:
            ip_address = '0.0.0.0'

        # Encode the IP address as a DNS response packet and send it back to the client
        response = ip_address.encode()
        sock.sendto(response, addr)
    except Exception as e:
        print('Error:', e)

    conn.close()
