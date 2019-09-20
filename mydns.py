def resolve(hostname):
    query_format = [
        "hex=id",
        "bin=flags",
        "uintbe:16=qdcount",
        "uintbe:16=ancount",
        "uintbe:16=nscount",
        "uintbe:16=arcount",
    ]

    query = {
        "id": 0x1a2b,
        "flags": 0b0000000100000000,
        "qdcount": 1,
        "ancount": 0,
        "nscount": 0,
        "arcount"
    }

    pass


def format_qname(hostname):
    hostname = hostname.split('.')
    idx = 0

    for i, h in enumerate(hostname):
        # Add length to the query format and body

        query_format.append('hex=qname{}'.format(idx))
        query['qname{}'.format(idx)] = hex(len(h))
        idx += 1

        # Add hostname to the query format and body

        query_format.append('hex=qname{}'.format(idx))
        query['qname{}'.format(idx)] = hex(ord(h))
        idx += 1





