import yeelight as yee
from light_server.light_controller.commands import Commands

class CommandSender:
    def CommandSender(self):
        self.device_info = self.__load_devices()
        self.all_devices = [yee.Bulb(ip) for ip in self.device_info.keys()]
        self.commands = Commands()

    def __load_devices(self) -> dict:
        with open("light_server/configured_devices.conf","r") as file:
            lines = file.readlines()
            all_bulbs = {}
            for line in lines:
                line = line.strip()
                current_bulb = ""
                if line[0] == "#":
                    current_bulb = line[1:]
                    all_bulbs.update({current_bulb: []})
                else:
                    all_bulbs.update({current_bulb: all_bulbs.get(current_bulb).append(line)})
            return all_bulbs


    def send(self, command: str) -> None:
        parsed_command, arguments = self.commands.get_command_with_params(command)
        
        for device in self.all_devices:
            device.get_properties
            function = device.__getattribute__(parsed_command)
            result = function(arguments)