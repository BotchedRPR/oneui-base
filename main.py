# main.py
# BotchedRPR - 2023-2023
import glob

from progress.bar import Bar

deviceInfoDict = {
    "SOC_NAME": "",
    "BOARD_BASE": "",
    "BOARD_REPLACE_CAMERAFEATURE": "",
    "BOARD_REPLACE_CAMERAFEATURE_PATH": "",
    "BOARD_HAS_BROKEN_WEAVER": "",
    "BOARD_NO_FABRIC_CRYPTO": "",
    "BOARD_SET_DPI_EXPLICITLY": "",
    "BOARD_DPI": "",
}

socInfoDict = {
    "SOC_REMOVE_SELINUX_MAPPINGS": "",
    "SOC_MIN_API_LEVEL": "",
    "SOC_TARGET_API_LEVEL": "",
}


def get_device_dirs(path):
    devices = []
    for files in glob.iglob(path + "**/*.device", recursive=True):
        print("[", len(devices), "] - ", files)
        devices.append(files)
    print("Found", len(devices), "devices.")
    return devices


def getDeviceInfo(path):
    file = open(path, "r")
    lines = file.readlines()
    fileBar = Bar('Processing device files...', max=len(lines))
    for line in lines:
        fileBar.next()
        if line.startswith("#"):
            continue
        if line.startswith("SOC_NAME"):
            deviceInfoDict["SOC_NAME"] = line.split(": ")[1].strip()
        if line.startswith("BOARD_BASE"):
            deviceInfoDict["BOARD_BASE"] = line.split(": ")[1].strip()
        if line.startswith("BOARD_REPLACE_CAMERAFEATURE") and not line.startswith("BOARD_REPLACE_CAMERAFEATURE_PATH"):
            deviceInfoDict["BOARD_REPLACE_CAMERAFEATURE"] = line.split(": ")[1].strip()
        if line.startswith("BOARD_REPLACE_CAMERAFEATURE_PATH"):
            deviceInfoDict["BOARD_REPLACE_CAMERAFEATURE_PATH"] = line.split(": ")[1].strip()
        if line.startswith("BOARD_HAS_BROKEN_WEAVER"):
            deviceInfoDict["BOARD_HAS_BROKEN_WEAVER"] = line.split(": ")[1].strip()
        if line.startswith("BOARD_NO_FABRIC_CRYPTO"):
            deviceInfoDict["BOARD_NO_FABRIC_CRYPTO"] = line.split(": ")[1].strip()
        if line.startswith("BOARD_SET_DPI_EXPLICITLY"):
            deviceInfoDict["BOARD_SET_DPI_EXPLICITLY"] = line.split(": ")[1].strip()
        if line.startswith("BOARD_DPI"):
            deviceInfoDict["BOARD_DPI"] = line.split(": ")[1].strip()
    fileBar.finish()
    file = open("soc/" + deviceInfoDict["SOC_NAME"] + "/" + deviceInfoDict["SOC_NAME"] + ".soc", "r")
    lines = file.readlines()
    fileBar = Bar('Processing soc files...', max=len(lines))
    for line in lines:
        fileBar.next()
        if line.startswith("#"):
            continue
        if line.startswith("SOC_REMOVE_SELINUX_MAPPINGS"):
            socInfoDict["SOC_REMOVE_SELINUX_MAPPINGS"] = line.split(": ")[1].strip()
        if line.startswith("SOC_MIN_API_LEVEL"):
            socInfoDict["SOC_MIN_API_LEVEL"] = line.split(": ")[1].strip()
        if line.startswith("SOC_TARGET_API_LEVEL"):
            socInfoDict["SOC_TARGET_API_LEVEL"] = line.split(": ")[1].strip()
    fileBar.finish()

def printDeviceInfo():
    print("\n--------------------------\nDevice Info:")
    print("SOC_NAME: ", deviceInfoDict["SOC_NAME"])
    print("BOARD_BASE: ", deviceInfoDict["BOARD_BASE"])
    print("BOARD_REPLACE_CAMERAFEATURE: ", deviceInfoDict["BOARD_REPLACE_CAMERAFEATURE"])
    print("BOARD_REPLACE_CAMERAFEATURE_PATH: ", deviceInfoDict["BOARD_REPLACE_CAMERAFEATURE_PATH"])
    print("BOARD_HAS_BROKEN_WEAVER: ", deviceInfoDict["BOARD_HAS_BROKEN_WEAVER"])
    print("BOARD_NO_FABRIC_CRYPTO: ", deviceInfoDict["BOARD_NO_FABRIC_CRYPTO"])
    print("BOARD_SET_DPI_EXPLICITLY: ", deviceInfoDict["BOARD_SET_DPI_EXPLICITLY"])
    print("BOARD_DPI: ", deviceInfoDict["BOARD_DPI"])

    print("\n--------------------------\nSOC Info:")
    print("SOC_REMOVE_SELINUX_MAPPINGS: ", socInfoDict["SOC_REMOVE_SELINUX_MAPPINGS"])
    print("SOC_MIN_API_LEVEL: ", socInfoDict["SOC_MIN_API_LEVEL"])
    print("SOC_TARGET_API_LEVEL: ", socInfoDict["SOC_TARGET_API_LEVEL"])
    print("\n--------------------------\nBuild begins now.")

if __name__ == '__main__':
    print("OneUI Ports: Getting device directories")

    dev = get_device_dirs("device/")

    if len(dev) == 0:
        exit()

    sel = int(input("Select a device by entering its number."))

    if dev[sel] is None:
        print("Invalid device selected.")
        exit()

    getDeviceInfo(dev[sel])

    printDeviceInfo()