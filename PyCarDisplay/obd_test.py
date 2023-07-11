# implementation of the obd module with dummy functions
# this is used for testing on a non-Raspberry Pi system

# commands
class commandsList:
    def __init__(self) -> None:
        self.RPM = 1
        self.SPEED = 2
        self.MAF = 3
        self.COMMANDED_EQUIV_RATIO = 4
        self.AMBIANT_AIR_TEMP = 5
        self.COOLANT_TEMP = 6
        self.DISTANCE_SINCE_DTC_CLEAR = 7
        self.RELATIVE_THROTTLE_POS = 8
        self.RUN_TIME = 9
    
commands = commandsList()

class valMagnitude:
    def __init__(self) -> None:
        self.magnitude = 1000

class Response:
    def __init__(self) -> None:
        self.value = valMagnitude()
        self.isNull = False

    def is_null(self) -> bool:
        return self.isNull

class Async:
    def __init__(self) -> None:
        self.watchCommands = []

    def watch(self, command) -> None:
        self.watchCommands.append(command)

    def start(self) -> None:
        pass
    
    def status(self) -> str:
        return "Connected"

    def query(self, command):
        response = Response()
        
        if self.status == "Not Connected":
            response.value.magnitude = 0
            response.isNull = True
            return response

        # get the command value
        if command == commands.RPM:
            response.value.magnitude = 1500
        elif command == commands.SPEED:
            response.value.magnitude = 50
        elif command == commands.MAF:
            response.value.magnitude = 10
        elif command == commands.COMMANDED_EQUIV_RATIO:
            response.value.magnitude = 1.1
        elif command == commands.AMBIANT_AIR_TEMP:
            response.value.magnitude = 68
        elif command == commands.COOLANT_TEMP:
            response.value.magnitude = 90
        elif command == commands.DISTANCE_SINCE_DTC_CLEAR:
            response.value.magnitude = 0
        elif command == commands.RELATIVE_THROTTLE_POS:
            response.value.magnitude = 15
        elif command == commands.RUN_TIME:
            response.value.magnitude = 0
        else:
            response.value.magnitude = 0
        
        return response
