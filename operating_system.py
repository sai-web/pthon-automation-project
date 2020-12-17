import abc
from pyautogui import press, hotkey, keyDown, keyUp
import sys
import os
import subprocess

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

# https://www.python-course.eu/python3_abstract_classes.php
# https://pycaw.readthedocs.io/en/latest/
class OS:
    @abc.abstractmethod
    def do_action(self, action: str) -> bool:
        """
        This method is meant to complete any given action for the corresponding os
        action - string of action to take
        """

    @abc.abstractmethod
    def status(self, value: str) -> str:
        """
        This method is meant to store the current active state of the user
        """

    @staticmethod
    def get_os() -> "instance":
        if sys.platform == "win32":
            return Windows()
        elif sys.platform.__contains__("darwin"):
            return MAC()
        elif sys.platform.__contains__("linux"):
            return Linux()
        else:
            raise Exception("unknown operating system")


##   Windows Operating System
class Windows(OS):
    name = "WINDOWS"

    def __init__(self):
        self.status = "not set"
        # self.audioDevides = AudioUtilities.GetSpeakers()
        # interface = self.audioDevides.Activate(
        #     IAudioEndpointVolume._iid_, CLSCTX_ALL, None
        # )
        # volume_control = cast(interface, POINTER(IAudioEndpointVolume))
        # print(self.audioDevides.)
        # print(volume_control.GetVolumeRange())

    def computeWifi(self) -> list:
        devices = subprocess.check_output(["netsh", "wlan", "show", "profiles"]).decode(
            "utf-8", errors="backslashreplace"
        )
        devices = devices.split("\n")
        names = []
        for i in devices:
            if "All User Profile" in i:
                i = i.split(":")
                i = i[1]
                i = i[1:-1]
                names.append(i)
        return names

    def connectWifi(self, wifi: str) -> str:
        try:
            subprocess.run(f"netsh wlan connect ssid={wifi} name={wifi}")
            return f"connected to {wifi}"
        except Exception:
            return "no such wifi"

    def computeBluetooth(self):
        pass

    def connectBluetooth(self):
        pass

    # def left(self):
    #     keyDown("win")
    #     keyDown("ctrl")
    #     press("left")
    #     keyUp("win")
    #     keyUp("ctrl")

    # def right(self):
    #     keyDown("win")
    #     keyDown("ctrl")
    #     press("right")
    #     keyUp("win")
    #     keyUp("ctrl")

    def do_action(self, action: str) -> bool:
        windowKeys = {
            "playpause": "playpause",
            "volumeup": "volumeup",
            "prevtrack": "prevtrack",
            "volumedown": "volumedown",
            "nexttrack": "nexttrack",
            "volumemute": "volumemute",
            "down": "down",
            "up": "up",
            "right": "right",
            "left": "left",
            "space": "space",
        }

        try:
            if action == "power":
                hotkey("alt", "f4")
            elif action in windowKeys:
                press(windowKeys[action])
            else:
                pass
                # print("unknown button") # prevents people from injecting keys in url ^ .

            return True
        except Exception:
            return False

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        self._status = value


##   Mac Operating System
class MAC(OS):

    name = "MAC"

    isMuted = False
    currentVolume = 5

    def __init__(self):
        self._status = "not set"

    def currentVolumeInfo(self):
        cmd = "osascript -e 'output volume of (get volume settings)'"
        s = subprocess.run(cmd, shell=True, capture_output=True)
        print(s)
        self.currentVolume = (
            int(s.stdout.decode().split()[0]) // 10
        )  # mapping value  of 0-100 to 0-10.

    def controllVolume(self, vc) -> None:

        if (
            self.currentVolume > 7 or self.currentVolume < 1
        ):  # adding restrictions (because of apple scripts err!)
            self.currentVolume = 0 if self.currentVolume < 1 else 7

        if vc == "volumedown":
            self.currentVolume -= 1

        if vc == "volumeup":
            self.currentVolume += 1

        os.system(f"osascript -e 'set volume {self.currentVolume}'")

    def muteMac(self) -> None:  # Mutes and unmutes fix.

        if not self.isMuted:
            os.system("osascript -e 'set volume output muted true'")
            self.isMuted = True
        else:
            os.system("osascript -e 'set volume output muted false'")
            self.isMuted = False

    def do_action(self, action: str) -> bool:

        # prevents people from injecting keys in url.
        macKeys = {
            "playpause": "space",
            "prevtrack": "left",
            "nexttrack": "right",
            "down": "down",
            "up": "up",
            "right": "right",
            "left": "left",
            "space": "space",
        }
        try:
            # print("action: ", action)
            if action == "power":
                hotkey("command", "q")
            elif action == "volumemute":
                self.muteMac()
            elif action == "volumeup" or action == "volumedown":
                self.controllVolume(action)
            elif action in macKeys:
                press(macKeys[action])
            else:
                # print("unknown button") # prevents people from injecting keys in url ^ .
                pass
            return True
        except Exception:
            return False

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        self._status = value


##   Linux Operating System
class Linux(OS):

    name = "LINUX"

    def __init__(self):
        self._status = "not set"

    def do_action(self, action: str) -> bool:
        linuxKeys = {
            "playpause": "space",
            "volumeup": "up",
            "prevtrack": "left",
            "volumedown": "down",
            "nexttrack": "right",
            "volumemute": "m",
            "down": "down",
            "up": "up",
            "right": "right",
            "left": "left",
            "space": "space",
        }
        try:
            if action == "power":
                hotkey("alt", "f4")
            elif action in linuxKeys:
                press(linuxKeys[action])
            else:
                # print("unknown button") # prevents people from injecting keys in url ^ .
                pass

            return True
        except Exception:
            return False

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        self._status = value
