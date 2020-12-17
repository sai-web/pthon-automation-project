import subprocess


def computeWifi():
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


print(computeWifi())