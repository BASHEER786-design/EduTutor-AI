import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Define the required scopes for Google Classroom
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly']

# Function to authenticate and build the service
def get_classroom_service():
    creds = None

    # Load saved credentials if available
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials, log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for future use
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('classroom', 'v1', credentials=creds)
    return service

# Function to list courses
def list_courses():
    service = get_classroom_service()
    results = service.courses().list(pageSize=10).execute()
    courses = results.get('courses', [])
    return courses
