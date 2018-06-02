import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re

# toCorrect is a hash consisting of records, which data is to be corrected
# its values are the wrong records and keys - row:column

toCorrect = []


def filter_records(arr):
    new_arr = []
    for x in arr:
        if x['studia'] != '---':
            new_arr.append(x)
    return new_arr


def correct_arr(arr):
    for x in arr:
        if not re.match('^s\d+$', x['studia']):
            toCorrect.append(x)
        elif not re.match('^\d+$', str(x['sem'])):
            toCorrect.append(x)
        elif x['pora'] not in 'LZ':
            toCorrect.append(x)
        elif x['typ'] not in 'WCPL':
            toCorrect.append(x)
        elif x['grupa'] and not re.match('^\d+$', str(x['grupa'])):
            toCorrect.append(x)
        elif not re.match('^\d+$', str(x['wym'])):
            toCorrect.append(x)
        elif x['miejsce'] and not re.match('^\w\d+ \S+$', x['miejsce']):
            toCorrect.append(x)


# connect to the spreadsheet

scope = ['http://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('MendrochPythonProject3-00c41c0a29cb.json', scope)

gc = gspread.authorize(credentials)

# open the spreadsheet

wks = gc.open('MendrochPythonProject3').sheet1.get_all_records()

# process the spreadsheet

wks = filter_records(wks)

# for i in wks:
#     print(i)

correct_arr(wks)

for i in toCorrect:
    print(i)
