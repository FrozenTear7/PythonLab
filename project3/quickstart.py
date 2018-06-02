import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['http://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('MendrochPythonProject3-00c41c0a29cb.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open('MendrochPythonProject3').sheet1

print(wks.get_all_records())
