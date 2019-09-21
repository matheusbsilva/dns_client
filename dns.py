import socket
import sys

import bitstring


def convert_to_hex(element):

    if isinstance(element, int):
        hex_element = hex(element)

        if element < 16:
            hex_element = "0x0%s" % hex_element[2:]

        return hex_element

    byte_element = element.encode('utf-8')
    hex_element = "0x%s" % byte_element.hex()

    return hex_element


def define_qtype_qclass(qtype, qclass, query_format, query):
    query_format.append("uintbe:16=qtype")
    query["qtype"] = qtype

    query_format.append("hex=qclass")
    query["qclass"] = qclass


def format_qname(hostname, query_format, query):
    hostname = hostname.split('.')
    idx = 0

    for i, h in enumerate(hostname):
        # Adiciona tamanho ao formato da query e o corpo

        query_format.append('hex=qname{}'.format(idx))
        query['qname{}'.format(idx)] = convert_to_hex(len(h))
        idx += 1

        # Adiciona o hostname ao formato da query e o corpo

        query_format.append('hex=qname{}'.format(idx))
        query['qname{}'.format(idx)] = convert_to_hex(h)
        idx += 1

    # Adiciona bit final
    query_format.append('hex=qname{}'.format(idx))
    query['qname{}'.format(idx)] = convert_to_hex(0)


def verify_rcode(response_bytes):

    rcode_offset = 28
    rcode_end = rcode_offset + 4
    response_code = str(response_bytes[rcode_offset:rcode_end].hex)

    if response_code == "1":
        print("Format error - The name server was unable to interpret the query.")
        sys.exit(1)

    elif response_code == "2":
        print("Server failure - The name server was unable to process this query due to a problem with the name server.")
        sys.exit(1)

    elif response_code == "3":
        print("Name Error - Meaningful only for responses from an authoritative name server, this code signifies that the domain name referenced in the query does not exist.")
        sys.exit(1)

    elif response_code == "4":
        print("Not Implemented - The name server does not support the requested kind of query.")
        sys.exit(1)

    elif response_code == "5":
        print("Refused - The name server refuses to perform the specified operation for policy reasons.")
        sys.exit(1)

    return True


def parse_rdata(response_bytes):

    ip1 = int(str(response_bytes[-32:-24]), 16)
    ip2 = int(str(response_bytes[-24:-16]), 16)
    ip3 = int(str(response_bytes[-16:-8]), 16)
    ip4 = int(str(response_bytes[-8:]), 16)

    return "%s.%s.%s.%s" % (ip1, ip2, ip3, ip4)


def resolve(hostname, dns_ip):
    qtype_A = 1
    qclass_IN = "0x0001"

    query_format = [
        "hex=id",
        "bin=flags",
        "uintbe:16=qdcount",
        "uintbe:16=ancount",
        "uintbe:16=nscount",
        "uintbe:16=arcount",
    ]

    query = {
        "id": "0x1a3b",
        "flags": "0b0000000100000000",
        "qdcount": 1,
        "ancount": 0,
        "nscount": 0,
        "arcount": 0
    }

    format_qname(hostname, query_format, query)
    define_qtype_qclass(qtype_A, qclass_IN, query_format, query)

    data = bitstring.pack(",".join(query_format), **query)

    dns_port = 53

    buffer_size = 1024

    address = (dns_ip, dns_port)

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    client.sendto(data.tobytes(), address)

    data, address = client.recvfrom(buffer_size)

    data = bitstring.BitArray(bytes=data)

    if verify_rcode(data):
        ipv4 = parse_rdata(data)
        print(hostname, "<>", ipv4)


if __name__ == '__main__':
    try:
        resolve(sys.argv[1], sys.argv[2])
        sys.exit(0)
    except IndexError:
        print("Argumentos inválidos!!!")
        sys.exit(1)
