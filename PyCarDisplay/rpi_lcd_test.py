# implementation of the rpi_lcd module with dummy functions
# this is used for testing on a non-Raspberry Pi system

class LCD:
    def __init__(self, address) -> None:
        pass

    def text(self, text, pos) -> None:
        print(text)

    def clear(self) -> None:
        pass