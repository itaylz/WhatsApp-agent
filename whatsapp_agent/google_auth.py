import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# These scopes dictate what the script is allowed to do.
# If you modify these scopes later, you MUST delete the token.json file to re-authenticate.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/calendar.events'
]

def get_google_credentials():
    """Handles OAuth 2.0 flow and returns valid Google credentials."""
    creds = None
    
    # token.json stores your access and refresh tokens. It is created 
    # automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    # If there are no (valid) credentials available, prompt the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired access token...")
            creds.refresh(Request())
        else:
            print("Initiating new OAuth flow...")
            # This looks for the credentials.json you downloaded from Google Cloud
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            # Opens a browser window for you to log in and grant permissions
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run so you don't have to log in every time
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    return creds

if __name__ == '__main__':
    # Run this file directly once to generate the token.json file.
    credentials = get_google_credentials()
    print("Authentication successful! token.json has been generated.")