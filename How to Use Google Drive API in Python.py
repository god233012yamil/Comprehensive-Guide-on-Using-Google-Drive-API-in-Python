import os.path
import io
import pickle
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

class GoogleDriveAPI:
    """Google Drive API class"""
    def __init__(self):
        creds = None
        if os.path.exists('token.pickle'):
            creds = self.load_credentials()
        if not creds or not creds.valid:
            creds = self.get_credentials()
        try:
            self.service = build('drive', 'v3', credentials=creds)
        except Exception as e:
            print(f"Failed to build service: {e}")

    def load_credentials(self):
        """Load user credentials from token.pickle"""
        try:
            with open('token.pickle', 'rb') as token:
                return pickle.load(token)
        except IOError as e:
            print(f"Failed to load credentials: {e}")

    def save_credentials(self, creds):
        """Save user credentials to token.pickle"""
        try:
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        except IOError as e:
            print(f"Failed to save credentials: {e}")

    def get_credentials(self):
        """Get user credentials"""
        creds = None
        if os.path.exists('token.pickle'):
            creds = Credentials.from_authorized_user_file('token.pickle', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            self.save_credentials(creds)
        return creds

    def list_files(self, pageSize=10):
        """List files in Google Drive"""
        try:
            results = self.service.files().list(
                pageSize=pageSize, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])
            return items
        except HttpError as error:
            print(f"An error occurred: {error}")

    def upload_file(self, filename, filepath, mimetype):
        """Upload file to Google Drive"""
        file_metadata = {'name': filename}
        media = MediaFileUpload(filepath, mimetype=mimetype)
        try:
            file = self.service.files().create(body=file_metadata,
                                               media_body=media,
                                               fields='id').execute()
            return file
        except HttpError as error:
            print(f"An error occurred: {error}")

    def download_file(self, file_id, filepath):
        """Download file from Google Drive"""
        request = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO(filepath, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        try:
            while done is False:
                status, done = downloader.next_chunk()
            return True if done else False
        except HttpError as error:
            print(f"An error occurred: {error}")

    def delete_file(self, file_id):
        """Delete file from Google Drive"""
        try:
            self.service.files().delete(fileId=file_id).execute()
            return True
        except HttpError as error:
            print(f"An error occurred: {error}")

# Example usage
if __name__ == '__main__':
    drive_api = GoogleDriveAPI()

    # Upload a file
    print("Uploading a file...")
    file_metadata = drive_api.upload_file("test.txt", "/path/to/test.txt", "text/plain")
    print(f"Uploaded file with ID {file_metadata['id']}")

    # List files
    print("Listing files...")
    items = drive_api.list_files()
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

    # Download a file
    print("Downloading a file...")
    success = drive_api.download_file(file_metadata['id'], "/path/to/download/test.txt")
    if success:
        print("File downloaded successfully")
    else:
        print("Failed to download file")

    # Delete a file
    print("Deleting a file...")
    drive_api.delete_file(file_metadata['id'])
    print("File deleted")
