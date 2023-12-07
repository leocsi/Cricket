import yeelight as yee
from light_controller.commands import CommandContext
from exceptions.light_server_exceptions import CommandNotFoundException

class CommandSender:
    def __init__(self):
        self.all_devices = []
        self.all_rooms = {}
        self.device_info = self.__load_devices()

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
        
        devices = {}
        try:
            if split_command[0] in self.all_rooms:
                devices = self.all_rooms[split_command[0]]
                command = split_command[1]
            else:
                devices = self.all_devices

            resolved_command = CommandContext(command)
            
        except CommandNotFoundException as e:
            print(e)

        for device in devices:
            try:
                function = device.__getattribute__(resolved_command.command)
                if resolved_command.stateful:
                    pass # Placeholder for potential stateful commands in the future

                if resolved_command.trueRandom:
                    result = function(resolved_command.args[0]())
                else:
                    result = function(*resolved_command.args)
                
            except Exception as e:
                print(e, "The exception occured when sending the command to: "+str(device))