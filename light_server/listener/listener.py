import socket

from light_server.light_controller.command_sender import CommandSender

class Listener:
    def Listener(self, host: str="127.0.0.1" , port: int=65432) -> None:
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
                        result = command_sender.send(data)

                    
