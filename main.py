"""
Made by Sai Sumith, Syed Safwan and Mahipathi

Project Started on: Feb 16, 2020

https://github.com/SyedSafwan

"""

from pyautogui import press, hotkey
from flask import Flask, render_template, request, jsonify
from time import sleep
import socket
import operating_system
import qrcode_terminal

# Fall back for unix devices. If you have fix to this issue please sumbit a pull request.
macKeys = {
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
}


def find_ip():
    """
    Returns local IP address of the machine.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))  # this sees if device is connected to internet
    ip = s.getsockname()[0]
    s.close()
    return ip


myOS = operating_system.OS.get_os()

issues = f"""
    Sorry, There seems to be a bug.
    Would you mind submitting an issue on the github repo?
    Please include this => {myOS.name} | {find_ip()}
    https://github.com/SyedSafwan/Phone-lord-
    """


def inialize():
    """
    Initializes ip address, port.
    Asks user if they want to view qr code.
    Checks if OS  is recognized or not.
    """
    ip = find_ip()
    port_num = 8000

    ask = input("do you want to see the qr Code? ")

    if ask.lower() == "y" or ask.lower() == "yes":
        qrcode_terminal.draw(f"http://{ip}:{port_num}")
    else:
        print("-" * 50 + "\n" * 5)
        print(f"Type this in Apple watch app =>  {ip}:{port_num}")
        print("\n" * 5 + "-" * 50)

    print("\n\nminimize this application\n\n")
    print("Your ip:", ip)
    print("Port:", port_num)
    print("OS:", myOS.name)

    return (ip, port_num)


ip, port_num = inialize()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/press")
def do_press():
    key = request.args.get("key", "None")

    success = myOS.do_action(key)
    if key == "playpause":
        myOS.status = "inactive"
    else:
        myOS.status = "active"
    # print("_________>   ",changeKeys, key)

    return {"press": success, "status": myOS.status}


@app.route("/wifi/<wifiName>", methods=["GET", "POST"])
def wifiHandler(wifiName):
    if request.method == "POST":
        return jsonify(myOS.connectWifi(wifiName))
    else:
        return jsonify(myOS.computeWifi())


# change the port to any number 8000 to 65534
app.run(host="0.0.0.0", port=port_num)
