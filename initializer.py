import json
import os

def main():
    settings = {
                "folderPath" : ""
                }
    dir_path = os.path.dirname(os.path.realpath(__file__))
    settingsPath = os.path.join(dir_path,"settings.json")
    if not os.path.isfile(settingsPath):
        settings["folderPath"] = input("Enter the path to the folder you want to watch: ")

        with open(settingsPath, 'w') as outfile:
            json.dump(settings, outfile)
        print("Settings written to ", settingsPath)
        return settings
    with open(settingsPath, 'r') as infile:
        settings = json.load(infile)
    return settings
if __name__=="__main__":
    main()
