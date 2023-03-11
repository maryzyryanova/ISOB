from client import Client


class Hacker(Client):
    def __init__(self, ip_address, tcp_port):
        super(Hacker, self).__init__(ip_address, tcp_port)

    def receive(self, package):
        return self._build_answer(package, "Hacker server payload")
