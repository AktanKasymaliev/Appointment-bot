import gspread
from oauth2client.service_account import ServiceAccountCredentials

#authorization
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('./creds.json', scope)
client = gspread.authorize(creds)

#open the google spreadsheet (where 'emails' is the name of my sheet)
sheet = client.open('emails')
sheet_instance = sheet.get_worksheet(0)
records_data = sheet_instance.get_all_records()

print(records_data)
