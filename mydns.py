import bitstring
import socket


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
        # Add length to the query format and body

        query_format.append('hex=qname{}'.format(idx))
        query['qname{}'.format(idx)] = convert_to_hex(len(h))
        idx += 1

        # Add hostname to the query format and body

        query_format.append('hex=qname{}'.format(idx))
        query['qname{}'.format(idx)] = convert_to_hex(h)
        idx += 1

    # Add end bit
    query_format.append('hex=qname{}'.format(idx))
    query['qname{}'.format(idx)] = convert_to_hex(0)


def resolve(hostname):
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
        "id": "0x1a2b",
        "flags": "0b0000000100000000",
        "qdcount": 1,
        "ancount": 0,
        "nscount": 0,
        "arcount": 0
    }

    format_qname(hostname, query_format, query)
    define_qtype_qclass(qtype_A, qclass_IN, query_format, query)

    print(query_format)
    print(query)

    data = bitstring.pack(",".join(query_format), **query)

    dns_ip = "8.8.8.8"
    dns_port = 53

    buffer_size = 1024

    address = (dns_ip, dns_port)

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    client.sendto(data.tobytes(), address)

    data, address = client.recvfrom(buffer_size)

    data = bitstring.BitArray(bytes=data)

    # According to RFC 1025 the header size is 97 bits
    # so goes from 0 to 96
    # header_size = 96

    rcode_offset = 28
    rcode_end = rcode_offset + 4

    response_code = str(data[rcode_offset:rcode_end].hex)

    print(data)
    print(response_code)


if __name__ == '__main__':
    resolve("www.google.com")
