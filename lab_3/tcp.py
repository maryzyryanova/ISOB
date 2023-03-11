class TCP:
    def __init__(self, source_port, destination_port, ip):
        self.ip = ip
        self.source_port = source_port
        self.destination_port = destination_port
        self.sequence = 0
        self.acknowledgment = 0
        self.offset = 20
        self.ns = None

        # Reserved
        self.cwr = None
        self.ece = None

        # Flags
        self.urg = None
        self.ack = False
        self.psh = None
        self.rst = False
        self.syn = False
        self.fin = False
        self.window_size = None
        self.checksum = 0
        self.urgent = None

    def __str__(self):
        return f"Source {self.ip.source_ip}:{self.source_port}, " \
               f"Destination {self.ip.destination_ip}:{self.destination_port}, " \
               f"Sequence: {self.sequence}, " \
               f"Ack: {self.acknowledgment}, " \
               f"Payload: '{self.ip.payload}'"

    def __repr__(self):
        return "\n".join(
            [
                f"IP: {self.ip}",
                f"Source_port: {self.source_port}",
                f"Destination: {self.destination_port}",
                f"Sequence: {self.sequence}",
                f"Acknowledgment: {self.acknowledgment}",
                f"Offset: {self.offset}",
                f"NS: {self.ns}",
                f"CWR: {self.cwr}",
                f"URG: {self.urg}",
                f"ACK: {self.ack}",
                f"PSH: {self.psh}",
                f"RST: {self.rst}",
                f"SYN: {self.syn}",
                f"FIN: {self.fin}",
                f"Window size: {self.window_size}",
                f"Checksum: {self.checksum}",
                f"Urgent: {self.urgent}",
            ]
        )
