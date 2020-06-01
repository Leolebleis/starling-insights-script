import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://mail.google.com/']

token_file_name = "token.pickle"


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if is_credentials():
        creds = return_credentials()
    # If there are no (valid) credentials available, let the user log in.
    if not is_credentials():
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file_name, 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])


def is_credentials():
    creds = None

    # Check if this is the right directory, otherwise change to that directory (depends where the function is called).
    if os.getcwd()[-5:] != "gmail":
        os.chdir("gmail")

    if os.path.abspath(token_file_name):
        return True
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        return False


def return_credentials():
    with open(token_file_name, 'rb') as token:
        return pickle.load(token)


if __name__ == '__main__':
    main()
