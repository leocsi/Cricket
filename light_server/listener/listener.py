import socket

from light_controller.command_sender import CommandSender
from exceptions.light_server_exceptions import *

class Listener:
    def __init__(self, host="127.0.0.1", port=65432) -> None:
        self.HOST = host
        self.PORT = port

    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            command_sender = CommandSender()
            s.bind((self.HOST, self.PORT))
            while True:
                s.listen()

                conn, addr = s.accept()
                with conn:
                    print(f"connected by {addr}")
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        data = data.decode('utf-8')
                        try:
                            result = command_sender.send(data)
                        except CommandNotFoundException as e:
                            print(e)
                    
