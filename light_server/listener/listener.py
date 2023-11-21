import socket,select
from OpenSSL import SSL, crypto

from light_controller.command_sender import CommandSender
from exceptions.light_server_exceptions import *
from security.security_manager import verify_cert

class Listener:
    def __init__(self, host="127.0.0.1", port=65432) -> None:
        self.HOST = host
        self.PORT = port
        self.socket = self.create_socket()
        
        self.command_sender = CommandSender()

    def listen(self):
        clients = {}

        while True:
            try:

                r,_ ,_ = select.select([self.socket]+list(clients.keys()), [], [])
            except:
                break

            for cli in r:
                if cli==self.socket:
                    cli, addr = self.socket.accept()
                    print(f"Connection from {addr}")
                    clients[cli] = addr
                else:
                    try:
                        data = cli.recv(1024).decode("utf-8")
                        result = self.command_sender.send(data)
                        
                    except (SSL.WantReadError, SSL.WantWriteError, SSL.WantX509LookupError):
                        pass
                    except SSL.ZeroReturnError:
                        print("Client disconnected.")
                        cli.close()
                    except (SSL.Error, Exception):
                        print("Something went wrong.")
                        cli.close()
                        del clients[cli]

        for cli in clients.keys():
            cli.close()
        self.socket.close()

    def create_socket(self):
        ctx = SSL.Context(SSL.TLSv1_2_METHOD)
        ctx.set_verify(SSL.VERIFY_PEER|SSL.VERIFY_FAIL_IF_NO_PEER_CERT, verify_cert)
        ctx.use_privatekey_file("light_server/security/certs/server.pkey",crypto.FILETYPE_PEM)
        ctx.use_certificate_file("light_server/security/certs/server.cert",crypto.FILETYPE_PEM)
        ctx.load_verify_locations("light_server/security/certs/ca.cert")

        server = SSL.Connection(ctx, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        server.bind((self.HOST, self.PORT))
        server.listen(3)
        server.setblocking(False)
        return server
