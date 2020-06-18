from __future__ import print_function
from time import sleep
#from gpiozero import MCP3008
import pickle
import os.path
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pprint import pprint

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
# https://docs.google.com/spreadsheets/d/1zZa5Oo7x5hI3Ys9hd9jTlGvE50XQVeouMpM2UcKfnBw/view#gid=0
SOLAR_SPREADSHEET_ID = os.environ['SOLAR_SPREADSHEET']
SOLAR_RANGE_NAME = os.environ['SOLAR_SHEET'] + '!' + os.environ['SOLAR_RANGE']

# TODO: Figure out why GPIO Zero cannot be found.
#
# PHOTO_SHADE = MCP3008(channel=3)
# PHOTO_SUN = MCP3008(channel=6)
# 
# pot = MCP3008(channel=0)
# therm = MCP3008(channel=2)
# lm35 = MCP3008(channel=4)
# therm2 = MCP3008(channel=5)

THERM_OVEN = os.environ['THERMAL_PROB']
THERM_AIR = os.environ['THERMAL_SENSOR']

def get_temp(sensor_file):
    found_data = False
    
    while found_data == False:
        with open(sensor_file, 'r') as sense_data:
            for line in sense_data:
                if line.strip()[-3:] == 'YES':
                    found_data = True
                data_location = line.find('t=')
                if data_location != -1:
                    temp = float(line[data_location+2:]) / 1000.0
                    found_data = True
        sleep(0.2)
    print('Temp: {}'.format(temp))
    return temp    

def append_current_temps(service):
    """Append current temperatures to spreadsheet.
    Adds the data and returns number of additions.
    """

    t = datetime.datetime.now()
    time_string = t.strftime('%Y-%m-%d %H:%M:%S')
    
    print('Timestamp: {}'.format(time_string))
    values = [
        [
            time_string, get_temp(THERM_OVEN), get_temp(THERM_AIR)
        ]
    ]
    body = {
        'values': values
    }

    # valueInputOption - USER_ENTERED
    result = service.spreadsheets().values().append(
        spreadsheetId=SOLAR_SPREADSHEET_ID, range=SOLAR_RANGE_NAME,
        valueInputOption="USER_ENTERED", body=body).execute()
    print('Debug: {} cells appended.'.format(result \
                                        .get('updates') \
                                        .get('updatedCells')))
    
def print_sheet_info(service):
    request = service.spreadsheets().get(spreadsheetId=SOLAR_SPREADSHEET_ID,
                                         ranges=None,
                                         includeGridData=None)
    values = request.execute()
    pprint(values)

def print_last_row(service):
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SOLAR_SPREADSHEET_ID,
                                range=SOLAR_RANGE_NAME).execute()
    values = result.get('values', [])
    print('Found {} rows.'.format(len(values)))
    print('Last row: {}, {}, {}'.format(values[-1][0], values[-1][1],
                                        values[-1][2]))
    print('')

def print_rows(service):
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SOLAR_SPREADSHEET_ID,
                                range=SOLAR_RANGE_NAME).execute()
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
    
def main():
    """Writes and reads using Sheets API.
    Prints values from specified spreadsheet.
    """

    creds = None
    
    print('SOLAR_SPREADSHEET_ID: {}'.format(SOLAR_SPREADSHEET_ID))
    print('SOLAR_RANGE_NAME: {}'.format(SOLAR_RANGE_NAME))
    print('THERM_OVEN: {}'.format(THERM_OVEN))
    print('THERM_AIR: {}'.format(THERM_AIR))

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

    #print_rows(service)

#     print_last_row(service)
#     print('Photo shade: {}'.format(PHOTO_SHADE.value))
#     print('Photo sun: {}'.format(PHOTO_SUN.value))

    #print_sheet_info(service)

if __name__ == '__main__':
    main()
