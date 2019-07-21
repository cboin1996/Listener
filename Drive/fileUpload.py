from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient import http
import os
import sys
import json
import logging
# logging setup
pathToFolder = '/home/christianboin/Programming/Python/Listener'
logger = logging.getLogger('fileUpload')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt='%(asctime)s %(name)s  %(levelname)-8s %(message)s',datefmt="%Y-%m-%d - %H:%M:%S")
fh = logging.FileHandler(os.path.join(pathToFolder, 'infoWatch.log'))
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)
class Drive:
    pathTogSettings = os.path.join(os.path.dirname(os.path.realpath(__file__)),'gSettings.json')
    def __init__(self, fileName, fullPathForFileToUpload):
        self.service = None
        self.fileName = fileName
        self.fullPathForFileToUpload = fullPathForFileToUpload
        self.gSettings = {}
        if os.path.isfile(self.pathTogSettings):
            with open(self.pathTogSettings, 'r') as in_file:
                self.gSettings = json.loads(in_file.read())
        else:
            self.gSettings['folderID'] = str(input("No settings detected.  Input your folder ID. "))
            self.gSettings['email'] = input("Enter your gmail. ")
            with open(self.pathTogSettings, 'w') as out_file:
                json.dump(self.gSettings, out_file)
    def authenticate(self):
        SCOPES = ['https://www.googleapis.com/auth/drive']
        SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)),'client_secrets.json')
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        self.service = build('drive', 'v3', credentials=credentials)

    def upload(self):
        file_metadata = {'name': self.fileName,
                         'parents' : [self.gSettings['folderID']]}
        media = http.MediaFileUpload(self.fullPathForFileToUpload,
                                mimetype='audio/jpeg')
        file = self.service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        file_id = file.get('id')
        logger.debug('File creation successful -- ID: %s' % file_id)
        return file_id
        # the body of the permission is set to a user permission, with owner responnsibility, and the email in settings.
        #self.service.permissions().create(fileId=file_id, body={'type': 'user', 'role' : 'owner', 'emailAddress' :  self.gSettings['email'], 'transerOwnership' : True}).execute()
if __name__=="__main__":
    driveSession = Drive()
    driveSession.authenticate()
    driveSession.upload()

