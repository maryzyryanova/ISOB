import time

from connection import Connection, print_package
from client import Client
from hacker import Hacker


class RSTMiddleware:
    def __init__(self):
        self.call_number = 0

    def change(self, package):
        self.call_number += 1
        if self.call_number == 5:
            package.rst = True
        return package


class TcpResetMiddleware:
    def __init__(self):
        self.call_number = 0

    def change(self, package):
        self.call_number += 1
        if self.call_number == 5:
            package.rst = False
        return package


class PassiveScan:
    def __init__(self):
        self.call_number = 0

    def change(self, package):
        self.call_number += 1
        if self.call_number >= 5 and self.call_number % 5 == 0:
            package.ip.payload = "Passive scan"
            print("Information: ", "syn:", package.syn, "ack:", package.ack, "rst:", package.rst)
        return package


class Sniffing:
    def __init__(self):
        self.call_number = 0

    def change(self, package):
        self.call_number += 1
        if self.call_number >= 5:
            package.ip.payload = "Sniffing"
            print("Information: ", repr(package))
        return package


class FakeIpAddressMiddleware:
    def __init__(self, ip_address, tcp_port):
        self.ip_address = ip_address
        self.tcp_port = tcp_port
        self.call_number = 0

    def change(self, package):
        self.call_number += 1
        if self.call_number == 5:
            package.ip.destination_ip = self.ip_address
            package.destination_port = self.tcp_port
        return package


class ConnectionHijack:
    def __init__(self):
        self.call_number = 0

    def change(self, package):
        self.call_number += 1
        if self.call_number >= 5:
            package.ip.payload = "Connection hijacked"
            t = package.sequence
            package.sequence = package.acknowledgment
            package.acknowledgment = t + len(package.ip.payload)
            package.ip.destination_ip = package.ip.source_ip
            package.destination_port = package.source_port
            print_package(package)
        return package


def run_attacks():
    client = Client(123, 1)
    server1 = Client(221, 3)
    server2 = Hacker(331, 2)

    tcp_reset_middleware = TcpResetMiddleware()
    sniffing = Sniffing()
    passive_scan = PassiveScan()
    fake_ip_address_middleware = FakeIpAddressMiddleware(331, 2)
    rst_middleware = RSTMiddleware()
    connection_hijack = ConnectionHijack()
    connection = Connection([client, server1, server2], [passive_scan])

    client.call_any_other(connection)


run_attacks()
