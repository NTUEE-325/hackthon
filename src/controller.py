import threading
import time
import sys
import serial


class bluetooth:
    def __init__(self, port: str, baudrate: int = 9600):
        """ Initialize an BT object, and auto-connect it. """
        # The port name is the name shown in control panel
        # And the baudrate is the communication setting, default value of HC-05 is 9600.
        self.ser = serial.Serial(port, baudrate=baudrate)

    def is_open(self) -> bool:
        return self.ser.is_open

    def waiting(self) -> bool:
        return self.ser.in_waiting

    def do_connect(self, port: str, baudrate: int = 9600) -> bool:
        """ Connect to the specify port with particular baudrate """
        # Connection function. Disconnect the previous communication, specify a new one.
        self.disconnect()

        try:
            self.ser = serial.Serial(port, baudrate=baudrate)
            return True
        except:
            return False

    def disconnect(self):
        """ Close the connection. """
        self.ser.close()

    def write(self, output: str):
        # Write the byte to the output buffer, encoded by utf-8.
        send = output.encode("utf-8")
        self.ser.write(send)

    def readString(self) -> str:
        # Scan the input buffer until meet a '\n'. return none if doesn't exist.
        if(self.waiting()):
            receiveMsg = self.ser.readline().decode("utf-8")[:-1]

        return receiveMsg


def read():
    if bt.waiting():
        print(bt.readString())


def write(msgWrite):

    print(msgWrite)

    if msgWrite == "exit":
        sys.exit()

    bt.write(msgWrite + "\n")


last_strength = 3  # record the last strength change [use in SetStrength()]
bt = bluetooth("COM4")
while not bt.is_open():
    pass
print("BT Connected!")

readThread = threading.Thread(target=read)
readThread.setDaemon(True)
readThread.start()


def SetMode(mode):
    # modes = ["normal", "study", "night", "gym"]
    if (mode == "normal"):
        write("d")
    elif (mode == "study"):
        write("s")
    elif (mode == "night"):
        write("n")
    elif (mode == "gym"):
        write("g")
    else:
        write("_")  # just a random char , mean nothing
    pass


def Set_Angle(x, y):
    # x is the horizontal angle, y is the vertical angle
    hor_angle = ""
    ver_angle = ""
    hor_angle = str(x)
    ver_angle = str(y)
    if len(hor_angle) == 1:
        hor_angle = "x00" + hor_angle
    elif len(hor_angle) == 2:
        hor_angle = "x0" + hor_angle
    elif len(hor_angle) == 3:
        hor_angle = "x" + hor_angle
    else:
        print("error in controller SetAngle!!!!")

    if len(ver_angle) == 1:
        ver_angle = "y00" + ver_angle
    elif len(ver_angle) == 2:
        ver_angle = "y0" + ver_angle
    elif len(ver_angle) == 3:
        ver_angle = "y" + ver_angle
    else:
        print("error in controller SetAngle!!!!")

    write(hor_angle)
    write(ver_angle)


def SetStrength(n):  # 為加強or減弱
    # range from 1~
    if n > last_strength and n <= 5:
        for i in range(n-last_strength):
            write('+')
    elif n < last_strength and n >= 1:
        for i in range(last_strength-n):
            write('-')
    else:
        pass
