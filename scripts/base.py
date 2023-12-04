# base.py
# BotchedRPR - 2023

# This file contains functions to extract and prepare a "porting base"
# for the ported device. This can include debloating as well as converting
# the partitions to EROFS, or from EROFS to EXT4 (not implemented yet).

import os
import magic
import tarfile
import lz4.frame
import subprocess

def extract_super(path):
    tar = tarfile.open(path)
    tar.extractall(members=[tar.getmember('super.img.lz4')])
    tar.close()

    lz4.frame.decompress('super.img.lz4', 'super.img')
    os.remove('super.img.lz4')
    os.rename("super.img", "../base/super.img")

    unpack_super("../base/super.img")

def unpack_super(path):
    os.mkdir("../base/unpacked")
    # Yeah yeah, I just did not want to modify lpunpack's argparse to be able to call its main.
    # Maybe I'll do it in the future.
    subprocess.run("../tools/lpunpack.py ../base/super.img ../base/unpacked")

def prepare_base(basetype, rootDir):
    base = ""
    for bases in os.listdir(rootDir + 'base/'):
        if bases.endswith('.img'):
            if basetype in bases:
                base = bases
                continue
            break
    if base == "":
        print("FATAL: No base image (", basetype, ") found. Exiting.")
        exit(1)

    path = rootDir + 'base/' + base
    # Base image filename should also contain the filesystem - but I digress. That's to be done later.
    fileType = magic.from_file(path)
    if "TAR" in fileType:
        extract_super(path)
    elif "Android sparse image" in fileType:
        unpack_super(path)