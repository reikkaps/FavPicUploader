#!/usr/bin/python3
#
# simple picture uploader for old school digital cameras without network devices
# using only python core modules
#
# version 0.0.1 ..... first public release (basic cmdline and functions)
# licence GPLv3
#
# Reiko Kaps 2010 r31k@k4p5.de


import xml.etree.ElementTree as ET
import argparse
import shutil, os

def getFavPictures(favfile):
    """
    read the print or fac file from sd card and
    parse the content
    @param:   favfile ... path the the file (absolute or relative)
    @return:  List of file pathes
    """
    try:
        data = ET.parse(favfile)
    except IOError as e:
        print('Error: {}'.format(e))
        return False

    filelist = []
    root = data.getroot()
    for neighbor in root.iter('file'):
        favPic = neighbor.find('path').text
        print('Found favorite picture {}'.format(favPic))
        filelist.append(favPic)

    return filelist
        
        
def checkDest(destFolder):
    """
    checks destination folder, if not exists and possible: create it
    @param:  destFolder .... path to the folder
    @return: boolean
    """
    if os.path.isdir(destFolder):
        print('Destination Folder {} exists'.format(destFolder))
        return True

    try:
        print('creating Destination Folder {}'.format(destFolder))
        os.mkdir(destFolder)
    except IOError as e:
        print('Error: {}'.format(e))
        return False

    return True
    


def copyPic(relpath, sourceFolder, destFolder):
    # get the real and normalized path of the picture
    sourcePath = os.path.normpath(os.path.join(sourceFolder, relpath))    
    print('copying picture {} to {}'.format(sourcePath, destFolder))
    try:
        shutil.copy2(sourcePath, destFolder)
    except IOError as e:
        print('Fehler: {}'.format(e))
        return False

    return True

def main():
    parser = argparse.ArgumentParser(description='Simple Picture Uploader which use the camera print or fav function to upload picture to disk',
                                     epilog='Currently only the Fav-Fileformat of Nikon cameras is supported \n(get the source: https://github.com/reikkaps/FavPicUploader)'
    )
    parser.add_argument('favfile', help='path to Nikons fav xml file on sdcard')
    parser.add_argument('destination', help='path to a destination folder on harddisk')
    args = parser.parse_args()

    # get the folder of the xml file
    sourcePath = os.path.abspath(args.favfile)
    sDir = os.path.dirname(sourcePath)
        
    if checkDest(args.destination):
        files = getFavPictures(args.favfile)
        for file in files:
            copyPic(file, sDir, args.destination)
    

if __name__ == '__main__':
    main()
    
