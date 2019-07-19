import json
import initializer
import os, time, sys


def get_size_of_file(filePath):
    if os.path.isfile(filePath):
        stat = os.stat(filePath)
        return stat.st_size

    else:
        return -1

def wait_until_file_downloaded(filePath):
    currentFileSize = get_size_of_file(filePath)
    print("Size of file is: ")
    time.sleep(2)
    while currentFileSize != get_size_of_file(filePath) or get_size_of_file(filePath) == 0:
        currentFileSize = get_size_of_file(filePath)
        sys.stdout.write('\r%s Bytes'%(currentFileSize))
        sys.stdout.flush()
        time.sleep(2)
    print("\nFile download is complete at ", filePath)

def main(clArguments):
    settings = initializer.main()
    watchPath = settings["folderPath"]
    print("watching folder %s" % (watchPath))
    before = [file for file in os.listdir(watchPath)]
    while True:
        time.sleep(int(clArguments))
        after = [file for file in os.listdir(watchPath)]
        addedFiles = [file for file in after if not file in before]
        removedFiles = [file for file in before if not file in after]
        if addedFiles: print("Added: ", addedFiles)
        if removedFiles: print("Removed: ", removedFiles)
        before = after
        for addedFile in addedFiles:
            pathToFile = os.path.join(watchPath,addedFile)
            wait_until_file_downloaded(filePath=pathToFile)
            # TODO: left off here 07182019.. need to either upload file to gdrive or send email with file.
        #print(before)
        #print(after)


if __name__=="__main__":
    main(sys.argv[1])
