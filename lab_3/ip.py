class IP:
    def __init__(self, source_ip, destination_ip, payload):
        self.version = 4
        self.ihl = 5
        self.dscp = None
        self.ecn = None
        self.total_length = 576
        self.id = None
        self.flags = None
        self.fragment_offset = None
        self.ttl = 15
        self.protocol = 6
        self.checksum = None
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.payload = payload

    def __str__(self):
        return f"IPv{self.version}"

    def __repr__(self):
        return "\n".join(
            [
                f"Version: {self.version}",
                f"IHL: {self.ihl}",
                f"DSCP: {self.dscp}",
                f"ECN: {self.ecn}",
                f"Total length: {self.total_length}",
                f"ID: {self.id}",
                f"Flags: {self.flags}",
                f"Fragment offset: {self.fragment_offset}",
                f"TTL: {self.ttl}",
                f"Protocol: {self.protocol}",
                f"Checksum: {self.checksum}",
                f"Source IP: {self.source_ip}",
                f"Destination IP: {self.destination_ip}",
                f"Parameters: {self.payload}",
            ]
        )
