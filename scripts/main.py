# main.py
# BotchedRPR - 2023

# This file contains functions that are a mess.
# I feel ashamed publishing this. I really do.

import glob
import os

from progress.bar import Bar
from base import prepase_base

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

# We will check it in main
rootDir = "../"


# Gets all the .device config files under the specified path. Returns a list of device paths.
def get_device_dirs(path):
    devices = []
    for files in glob.iglob(path + "**/*.device", recursive=True):
        print("[", len(devices), "] - ", files)
        devices.append(files)
    print("Found", len(devices), "devices.")
    return devices


# This function was supposed to be easy-peasy and good-looking. It's not. It looks awful. Does it work? Yes.
def getDeviceInfo(path):
    file = open(path, "r")

    # Device properties
    lines = file.readlines()
    fileBar = Bar('Processing device files...', max=len(lines))
    comment = '#'

    for line in lines:
        fileBar.next()
        if line.startswith(comment):
            continue

        # Now we know that this isn't a comment, but we still need to rip out the comments that exist in the line.
        if comment in line:
            line = line.split(comment)[0]

        # Now we can process the property.
        if line.startswith("SOC_NAME"):
            deviceInfoDict["SOC_NAME"] = line.split(": ")[1].strip()
            continue
        if line.startswith("BOARD_BASE"):
            deviceInfoDict["BOARD_BASE"] = line.split(": ")[1].strip()
            continue
        if line.startswith("BOARD_REPLACE_CAMERAFEATURE") and not line.startswith("BOARD_REPLACE_CAMERAFEATURE_PATH"):
            deviceInfoDict["BOARD_REPLACE_CAMERAFEATURE"] = line.split(": ")[1].strip()
            continue
        if line.startswith("BOARD_REPLACE_CAMERAFEATURE_PATH"):
            deviceInfoDict["BOARD_REPLACE_CAMERAFEATURE_PATH"] = line.split(": ")[1].strip()
            continue
        if line.startswith("BOARD_HAS_BROKEN_WEAVER"):
            deviceInfoDict["BOARD_HAS_BROKEN_WEAVER"] = line.split(": ")[1].strip()
            continue
        if line.startswith("BOARD_NO_FABRIC_CRYPTO"):
            deviceInfoDict["BOARD_NO_FABRIC_CRYPTO"] = line.split(": ")[1].strip()
            continue
        if line.startswith("BOARD_SET_DPI_EXPLICITLY"):
            deviceInfoDict["BOARD_SET_DPI_EXPLICITLY"] = line.split(": ")[1].strip()
            continue
        if line.startswith("BOARD_DPI"):
            deviceInfoDict["BOARD_DPI"] = line.split(": ")[1].strip()
            continue
        elif line != "\n":  # If it's not any property, nor a comment, nor a blank line, it's bad.
            print("Unknown board property: ", line)
            exit(1)

    fileBar.finish()

    # SoC properties
    file = open(rootDir + "soc/" + deviceInfoDict["SOC_NAME"] + "/" + deviceInfoDict["SOC_NAME"] + ".soc", "r")
    lines = file.readlines()
    fileBar = Bar('Processing SoC files...', max=len(lines))
    for line in lines:
        fileBar.next()

        if line.startswith("#"):
            continue

        # Now we know that this isn't a comment, but we still need to rip out the comments that exist in the line.
        if comment in line:
            line = line.split(comment)[0]

        # Now we can process the property.
        if line.startswith("SOC_REMOVE_SELINUX_MAPPINGS"):
            socInfoDict["SOC_REMOVE_SELINUX_MAPPINGS"] = line.split(": ")[1].strip()
            continue
        if line.startswith("SOC_MIN_API_LEVEL"):
            socInfoDict["SOC_MIN_API_LEVEL"] = line.split(": ")[1].strip()
            continue
        if line.startswith("SOC_TARGET_API_LEVEL"):
            socInfoDict["SOC_TARGET_API_LEVEL"] = line.split(": ")[1].strip()
            continue

        elif line != "\n":
            print("Unknown SoC property: ", line)
            exit(1)

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
    if os.path.isfile("../build.sh"):
        print("Root directory is ../")
    else:
        print("Unable to find root directory.")

    print("OneUI Ports: Getting device directories")

    dev = get_device_dirs(rootDir + "device/")

    if len(dev) == 0:
        exit()

    sel = int(input("Select a device by entering its number. "))

    if dev[sel] is None:
        print("Invalid device selected.")
        exit()

    getDeviceInfo(dev[sel])

    printDeviceInfo() # Debug purposes? Nah. Keep with AOSP style? Maybe.

    prepare_base(deviceInfoDict["BOARD_BASE"], rootDir)
