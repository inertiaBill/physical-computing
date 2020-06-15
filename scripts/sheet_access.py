from __future__ import print_function
import pickle
import os.path
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
# https://docs.google.com/spreadsheets/d/1zZa5Oo7x5hI3Ys9hd9jTlGvE50XQVeouMpM2UcKfnBw/view#gid=0
SOLAR_OVEN_SPREADSHEET_ID = '1zZa5Oo7x5hI3Ys9hd9jTlGvE50XQVeouMpM2UcKfnBw'
SOLAR_OVEN_RANGE_NAME = 'Dev!A2:C'
SOLAR_OVEN_SHEET_NAME = 'Dev'

def append_current_temps(service):
    """Append current temperatures to spreadsheet.
    Adds the data and returns number of additions.
    """

    t = datetime.datetime.now()
    time_string = t.strftime('%Y-%m-%d %H:%M:%S')
    
    print('Timestamp: {}'.format(time_string))
    values = [
        [
            time_string, 44, 19
        ]
    ]
    body = {
        'values': values
    }

    # valueInputOption - USER_ENTERED
    result = service.spreadsheets().values().append(
        spreadsheetId=SOLAR_OVEN_SPREADSHEET_ID, range=SOLAR_OVEN_RANGE_NAME,
        valueInputOption="USER_ENTERED", body=body).execute()
    print('Debug: {} cells appended.'.format(result \
                                        .get('updates') \
                                        .get('updatedCells')))                                        

def main():
    """Writes and reads using Sheets API.
    Prints values from specified spreadsheet.
    """

    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Add current values to sheet
    append_current_temps(service)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SOLAR_OVEN_SPREADSHEET_ID,
                                range=SOLAR_OVEN_RANGE_NAME).execute()
    values = result.get('values', [])

    # Output spreadsheet data
    # TODO: Can we output just last few rows?
    # TODO: Should we output everytime?
    if not values:
        print('Warning: No data found')
    else:
        print('Time, Inside, Outside')
        for row in values:
            # Print columns A through C, which correspond to indices 0, 1, 2.
            print('{}, {}, {}'.format(row[0], row[1], row[2]))

if __name__ == '__main__':
    main()