import os

def checkFolder(folder, prefix):
    exit = False
    for foldername in os.listdir(prefix):
        if foldername == folder:
            exit = True
            break
    if not(exit) :
        os.makedirs(prefix + folder)

def checkFile(file, folder):
    exit = False
    for filename in os.listdir(folder):
        if filename == file:
            exit = True
            break
    return exit