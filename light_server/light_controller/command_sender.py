import yeelight as yee
from light_controller.commands import Commands

class CommandSender:
    def __init__(self):
        self.all_devices = []
        self.all_rooms = {}
        self.device_info = self.__load_devices()
        self.commands = Commands()

    def __load_devices(self) -> dict:
        with open("light_server/configured_devices.conf","r") as file:
            lines = file.readlines()
            all_bulbs = {}
            current_bulb = ""
            counter = 0
            for line in lines:
                line = line.strip()
                if line[0] == "#":
                    current_bulb = line[1:]
                    all_bulbs.update({current_bulb: []})
                    self.all_devices.append(yee.Bulb(current_bulb))
                    counter = 0
                else:
                    all_bulbs.get(current_bulb).append(line)
                    if counter == 1:
                        if line in self.all_rooms:
                            self.all_rooms[line].append(self.all_devices[-1])
                        else:
                            self.all_rooms.update({line: [self.all_devices[-1]]})
                counter += 1
            return all_bulbs


    def send(self, command: str) -> None:
        split_command = command.split()
        
        if split_command[0] in self.all_rooms:
            parsed_command, arguments = self.commands.get_command_with_params(split_command[1])
            devices = self.all_rooms[split_command[0]]
        
        else:
            parsed_command, arguments = self.commands.get_command_with_params(command)
            devices = self.all_devices

        for device in devices:
            try:
                function = device.__getattribute__(parsed_command)
                result = function(arguments)
            except Exception as e:
                print(e, "The exception occured when sending the command to: "+str(device))