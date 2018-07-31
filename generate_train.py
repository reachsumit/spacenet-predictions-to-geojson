import os
JPG_DIRECTORY = "output"
files = os.listdir(JPG_DIRECTORY)
files = [os.path.join(os.getcwd(),JPG_DIRECTORY,file) for file in files]
with open("train.txt","w") as thefile:
    for file in files:
        thefile.write("{}\n".format(file))