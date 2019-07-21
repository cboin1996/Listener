import json
import initializer
import os, time, sys
from Drive import fileUpload
import logging
from Messaging import Message
# setup a logging.
pathToFolder = os.path.dirname(os.path.realpath(__file__))

logger = logging.getLogger('watch.py')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt='%(asctime)s %(name)s  %(levelname)-8s %(message)s',datefmt="%Y-%m-%d - %H:%M:%S")
fh = logging.FileHandler(os.path.join(pathToFolder, 'infoWatch.log'))
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)
def get_size_of_file(filePath):
    if os.path.isfile(filePath):
        stat = os.stat(filePath)
        return stat.st_size

    else:
        return -1

def wait_until_file_downloaded(filePath):
    currentFileSize = get_size_of_file(filePath)
    logger.info("Size of file is: ")
    time.sleep(2)
    while currentFileSize != get_size_of_file(filePath) or get_size_of_file(filePath) == 0:
        currentFileSize = get_size_of_file(filePath)
        logger.info('%s Bytes'%(currentFileSize))
        time.sleep(2)
    logger.info("File download is complete at %s" % (filePath))

def main(clArguments, formatKey="_complt"):
    settings = initializer.main()
    watchPath = settings["folderPath"]
    logger.info("watching folder %s" % (watchPath))
    before = [file for file in os.listdir(watchPath)]
    while True:
        time.sleep(int(clArguments))
        after = [file for file in os.listdir(watchPath)]
        addedFiles = [file for file in after if not file in before]
        removedFiles = [file for file in before if not file in after]
        if addedFiles: logger.info("Added: %s"% (addedFiles))
        if removedFiles: logger.info("Removed: %s"% (removedFiles))
        before = after
        # iterate list of added files, add to gdrive and send text to notify user
        for addedFile in addedFiles:
        # check for "_formatted" in filename
            if formatKey in addedFile: 
                pathToFile = os.path.join(watchPath,addedFile)
                wait_until_file_downloaded(filePath=pathToFile)
                uploadToGDrive = fileUpload.Drive(fileName=addedFile, fullPathForFileToUpload=pathToFile)
                uploadToGDrive.authenticate()
                file_id = uploadToGDrive.upload()
                messager = Message.Messager()
                messager.createSMS("File Uploaded to Drive -- %s \n With ID -- %s" % (addedFile, file_id))
                os.remove(pathToFile)
            else:
                logger.info("File was never marked _complt.  Check ytdl to see why.")
        

if __name__=="__main__":
    main(sys.argv[1])
