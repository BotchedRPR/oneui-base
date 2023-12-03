# base.py
# BotchedRPR - 2023

# This file contains functions to extract and prepare a "porting base"
# for the ported device. This can include debloating as well as converting
# the partitions to EROFS, or from EROFS to EXT4 (not implemented yet).

import os

def prepase_base(type):
    base = ""
    baseType = ""
    for bases in os.listdir('.'):
        if bases.endswith('.img'):
            print("Base image found: ", bases)
            base = bases
            break
    if base == "":
        print("FATAL: No base image found. Exiting.")
        exit(1)
    if type not in base:
        print("FATAL: Base image: ", base, " is not for the specified device. Exiting.")
        exit(1)

    # Base image filename should also contain the filesystem - but I digress. That's to be done later.