"""
USAGE: python Imagetool.py <the absolute path of the directory containing raw images>  <the Full of the output directory>
"""

# ! /usr/bin/python
import sys, os

NameList = []

"""
check the extension of the all images
"""
def checkExtension(file):
    # set supported raw conversion extensions!
    fileExtension = ['.dng', '.raw', '.cr2', '.crw', '.erf', '.raf', '.tif', '.kdc', '.dcr', '.mos',
                     '.mef', '.nef', '.orf', '.rw2', '.pef', '.x3f', '.srw', '.srf', '.sr2', '.arw',
                     '.mdc', '.mrw']

    for i in fileExtension:
        if file.lower().endswith(i):
            return 'RAW'
    return 'notraw'


# find all the RAW files in the pass directory and all subDirectories
def checkDirectory(directory):
    list = []
    for path, subdir, files in os.walk(directory):
        for name in files:
            if checkExtension(name) == 'RAW':
                list.append(os.path.join(path, name))
                NameList.append(name)
                print(os.path.join(path, name))
    return list

#the main converting process
def main():
    raw_images = checkDirectory(sys.argv[1])
    words = [w.replace('[-4:0]', '.ppm') for w in NameList]
    for ele in range(len(raw_images)):
        newFormat = words[ele][0:-4] + ".PNG"
        outputdirectory = os.path.join(sys.argv[2], newFormat)
        os.system("dcraw -c {0} | pnmtopng >>{1}".format(raw_images[ele], outputdirectory))


if __name__ == '__main__':
    main()
