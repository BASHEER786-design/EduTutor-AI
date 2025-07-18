from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load service account credentials
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly']
SERVICE_ACCOUNT_FILE = 'credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the classroom service
service = build('classroom', 'v1', credentials=credentials)

# Fetch the list of active courses
def list_courses():
    results = service.courses().list(pageSize=10).execute()
    courses = results.get('courses', [])

    if not courses:
        print("No courses found.")
    else:
        print("Courses:")
        for course in courses:
            print(f"{course['name']} (ID: {course['id']})")

if __name__ == '__main__':
    list_courses()
