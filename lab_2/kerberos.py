import random
import time

from des import DES


def current_time_in_milliseconds():
    return int(round(time.time() * 1000))


def convert_hour_to_milliseconds(hour):
    return hour * 3_600_000


def create_key():
    return random.randint(100_000_000, 999_999_999)


class KDC:
    available_clients = ["client1", "client2"]
    clients_keys = [create_key(), create_key()]
    available_servers = ["server1", "server2"]
    server_keys = [create_key(), create_key()]

    def __init__(self):
        self.cipher_algorithm = DES()
        self.tgs_id = 1
        self.key_tgs = create_key()

    def get_permission_ticket(self, client_id):
        print("Call for getting new permission ticket")
        if client_id in self.available_clients:
            t = current_time_in_milliseconds()
            p = convert_hour_to_milliseconds(48)
            key_tgs_c = create_key()
            ticket = (client_id, self.tgs_id, t, p, key_tgs_c)
            print("New permission ticket:", ticket)

            encrypted_ticket = self.cipher_algorithm.encrypt(ticket, self.key_tgs)
            bundle = (encrypted_ticket, key_tgs_c)

            index = self.available_clients.index(client_id)
            client_key = self.clients_keys[index]
            encrypted_bundle = self.cipher_algorithm.encrypt(bundle, client_key)

            return encrypted_bundle

        print("Unknown client_id:", client_id)

    def get_server_ticket(self, permission_ticket, authority, server_id):
        print("Call for getting new server ticket")
        permission_ticket = self.cipher_algorithm.decrypt(
            permission_ticket, self.key_tgs
        )
        client_id, key_tgs_c = permission_ticket[0], permission_ticket[4]
        t, p = permission_ticket[2], permission_ticket[3]

        print(
            f"Permission ticket data. Client id: {client_id}, timestamp: {t},"
            f" period: {p}, key TGS-Client: {key_tgs_c}"
        )

        authority = self.cipher_algorithm.decrypt(authority, key_tgs_c)
        auth_client_id = authority[0]
        auth_t = authority[1]

        print(f"Authority data. Client id: {auth_client_id}, timestamp: {auth_t}")

        if client_id != auth_client_id:
            print("Invalid client")
            return None

        if auth_t < t or auth_t > t + p:
            print("Ticket is expired")
            return None

        t = current_time_in_milliseconds()
        p = convert_hour_to_milliseconds(48)
        key_ss_c = create_key()
        server_ticket = (client_id, server_id, t, p, key_ss_c)
        print("New server ticket:", server_ticket)

        index = self.available_servers.index(server_id)
        server_key = self.server_keys[index]
        encrypted_server_ticket = self.cipher_algorithm.encrypt(
            server_ticket, server_key
        )
        bundle = (encrypted_server_ticket, key_ss_c)
        encrypted_bundle = self.cipher_algorithm.encrypt(bundle, key_tgs_c)

        return encrypted_bundle


class Client:
    def __init__(self, client_id, client_key, kdc, server):
        self.client_id = client_id
        self.client_key = client_key
        self.kdc = kdc
        self.servers = server
        self.cipher_algorithm = DES()
        self.permission_ticket = None
        self.key_tgs_c = None

    def make_server_call(self, server_number):
        print("\nCall server", server_number)
        server = self.servers[server_number]

        if self.permission_ticket is None or self.key_tgs_c is None:
            print("Trying to get permission ticket")
            permission_ticket_bundle = self.kdc.get_permission_ticket(self.client_id)
            if permission_ticket_bundle is None:
                return None

            permission_ticket_bundle = self.cipher_algorithm.decrypt(
                permission_ticket_bundle, self.client_key
            )
            permission_ticket, key_tgs_c = (
                permission_ticket_bundle[0],
                permission_ticket_bundle[1],
            )
            print("Key TGS-Client:", key_tgs_c)

            self.permission_ticket = permission_ticket
            self.key_tgs_c = key_tgs_c
        else:
            print("Permission ticket and key TGS-Client already defined")
            permission_ticket = self.permission_ticket
            key_tgs_c = self.key_tgs_c

        print("Trying to get server ticket")
        bundle = self.call_tgs(permission_ticket, key_tgs_c, server.server_id)

        if bundle is None:
            return None

        bundle = self.cipher_algorithm.decrypt(bundle, key_tgs_c)
        server_ticket, key_ss_c = bundle[0], bundle[1]
        print("Key Server-Client:", key_ss_c)

        print("Trying connect to server")
        t = current_time_in_milliseconds()
        authority = (self.client_id, t)
        authority_encrypted = self.cipher_algorithm.encrypt(authority, key_ss_c)
        confirm_t = server.connect(server_ticket, authority_encrypted)

        if confirm_t is None:
            return

        confirm_t = self.cipher_algorithm.decrypt(confirm_t, key_ss_c)
        if confirm_t != t + 1:
            print("Server returns wrong confirmation timestamp")
            return

        print("Server call is successful")

    def call_tgs(self, permission_ticket, key_tgs_c, server_id):
        t = current_time_in_milliseconds()
        print(f"Call TGS. Server id: {server_id}, timestamp: {t}")
        authority = (self.client_id, t)
        authority_encrypted = self.cipher_algorithm.encrypt(authority, key_tgs_c)
        bundle = self.kdc.get_server_ticket(
            permission_ticket, authority_encrypted, server_id
        )

        return bundle


class Server:
    def __init__(self, server_id, server_key):
        self.server_id = server_id
        self.server_key = server_key
        self.cipher_algorithm = DES()

    def connect(self, server_ticket, authority):
        print("New server connection")
        server_ticket = self.cipher_algorithm.decrypt(server_ticket, self.server_key)
        client_id, server_id = server_ticket[0], server_ticket[1]
        t, p, key_ss_c = server_ticket[2], server_ticket[3], server_ticket[4]

        print(
            "Server ticket data. Client id: {client_id}, timestamp: {t}, "
            "period: {p}, key Server-Client: {key_ss_c}"
        )

        if server_id != self.server_id:
            print("Wrong server")
            return None

        authority = self.cipher_algorithm.decrypt(authority, key_ss_c)
        auth_client_id, auth_t = authority[0], authority[1]

        print(f"Authority data. Client id: {auth_client_id}, timestamp: {auth_t}")

        if client_id != auth_client_id:
            print("Invalid client")
            return None

        if auth_t < t or auth_t > t + p:
            print("Ticket is expired")
            return None

        confirm_t = auth_t + 1
        print("Confirmation timestamp is", confirm_t)
        encrypted_confirm_t = self.cipher_algorithm.encrypt(confirm_t, key_ss_c)

        return encrypted_confirm_t


def processing():
    kdc = KDC()
    server_1 = Server(kdc.available_servers[0], kdc.server_keys[0])
    server_2 = Server(kdc.available_servers[1], kdc.server_keys[1])
    client = Client(
        'client5', kdc.clients_keys[0], kdc, [server_1, server_2]
    )

    print(f"server0 id: {server_1.server_id}, server0 key: {server_1.server_key}")
    print(f'server1 id: {server_2.server_id}, server1" key: {server_2.server_key}')
    print(f"Client id: {client.client_id}, Client key: {client.client_key}")

    client.make_server_call(0)
    client.make_server_call(1)


if __name__ == "__main__":
    processing()
