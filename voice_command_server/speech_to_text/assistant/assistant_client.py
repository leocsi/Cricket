import socket
from speech_to_text.assistant.assistant_instructions import InstructionResolver

class AssistantClient:
    HOST = "127.0.0.1"
    PORT = 65432

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((AssistantClient.HOST, AssistantClient.PORT))
        self.sender = InstructionResolver()

    def send(self, command):
        resolved_commands = self.sender.get_command_suite(command)
        for command in resolved_commands:
            self.socket.sendall(bytes(command, "utf-8"))
