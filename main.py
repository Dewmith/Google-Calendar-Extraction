from __future__ import print_function
from datetime import datetime
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dateutil import parser

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def authenticate_google_calendar():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r"H:\.shortcut-targets-by-id\1-576puQIwu8kpP84GyiGMt0A3QjjQ55r\Google Drive\IT\Google Callendar Event Extraction\credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    service = build('calendar', 'v3', credentials=creds)
    return service


def calculate_work_hours(service, keyword, calendar_id='primary', time_min=None, time_max=None):
    
    '''if not time_min:
        time_min = datetime.datetime.utcnow().isoformat() + 'Z'
    if not time_max:
        time_max = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat() + 'Z'
        '''
    events_result = service.events().list(calendarId=calendar_id, timeMin=time_min,
                                          timeMax=time_max, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    total_hours = 0
    for event in events:
        if keyword.lower() == event['summary'].lower():
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            start_dt = parser.isoparse(start)
            end_dt = parser.isoparse(end)
            duration = end_dt - start_dt
            total_hours += duration.total_seconds() / 3600  # Convert seconds to hours
    
    return total_hours

def check_date(date_str):
    try:
        # Try to parse the date string using the given format
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        # If a ValueError is raised, the date is not in the correct format or is invalid
        print("Enter Correct Date Format!")
        print("")
        main()


def date_inorder(time_min_str, time_max_str):
    try:
        # Parse the date strings into datetime objects
        time_min = datetime.strptime(time_min_str, '%Y-%m-%dT%H:%M:%S%z')
        time_max = datetime.strptime(time_max_str, '%Y-%m-%dT%H:%M:%S%z')

        # Check if time_min is less than or equal to time_max
        if time_min > time_max:
            print("Invalid Date Range! 'time_min' is after 'time_max'!")
            print()
            main()
        else:
            return True

    except ValueError as e:
        print("Error parsing dates:", e)
        return False

def leaving():
    if (input("Press Enter to exit, anything else to search events again: ")) == "":
        exit()
    else:
        print()
        main()

def main():
    service = authenticate_google_calendar()
    # Replace with your desired time range
    time_min_sufix = 'T00:00:00Z'
    time_min_prefix = (input("Enter starting date (Eg: 2024-08-26):"))
    check_date(time_min_prefix) 
    time_min = time_min_prefix + time_min_sufix

    time_max_sufix = 'T23:59:59Z'
    time_max_prefix = (input("Enter ending date (Eg: 2024-08-26):"))
    check_date(time_max_prefix)
    time_max =  time_max_prefix + time_max_sufix

    #Check date order
    date_inorder(time_min,time_max)

    #Get evet name
    keyword = input("Enter Event Name: ")


    total_hours = calculate_work_hours(service,keyword, time_min=time_min, time_max=time_max)
    print(f"Total hours: {total_hours} hours")

    #Exiting
    leaving()
    

if __name__ == '__main__':
    main()
    
