import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re

# toCorrect is a hash consisting of records, which data is to be corrected
# its values are the wrong records and keys - row:column

toCorrect = []
lecturers = {}


def filter_records(arr):
    new_arr = []
    for i in range(0, len(arr)):
        if arr[i]['studia'] != '---':
            if arr[i]['osoba'] and arr[i]['osoba'] not in lecturers:
                lecturers[arr[i]['osoba']] = []

            new_obj = {}
            new_obj['row'] = i + 1
            new_obj['record'] = arr[i]

            new_arr.append(new_obj)
    return new_arr


def push_to_to_correct(x, error_type):
    new_obj = x
    new_obj['error'] = error_type
    toCorrect.append(new_obj)


def check_day(day):
    days = ['Pn', 'Wt', 'Sr', 'Cz', 'Pt']
    if day not in days:
        return False
    else:
        return True


def correct_arr(arr):
    for x in arr:
        record = x['record']
        if record['osoba']:
            lecturers[record['osoba']].append(record)

        if not re.match('^s\d+$', record['studia']):
            push_to_to_correct(x, 'studia')
        elif not re.match('^\d+$', str(record['sem'])):
            push_to_to_correct(x, 'sem')
        elif record['pora'] not in 'LZ':
            push_to_to_correct(x, 'pora')
        elif record['typ'] not in 'WCPL':
            push_to_to_correct(x, 'typ')
        elif record['grupa'] and not re.match('^\d+$', str(record['grupa'])):
            push_to_to_correct(x, 'grupa')
        elif not re.match('^\d+$', str(record['wym'])):
            push_to_to_correct(x, 'wym')
        elif record['miejsce'] and not re.match('^\w\d+ \S+$', record['miejsce']):
            push_to_to_correct(x, 'miejsce')
        elif record['tyg'] and not str(record['tyg']) in '12AB':
            push_to_to_correct(x, 'miejsce')
        elif record['dzien'] and not check_day(record['dzien']):
            push_to_to_correct(x, 'wym')
        elif record['godz'] and not re.match('^\d{2}:\d{2}$', str(record['godz'])):
            push_to_to_correct(x, 'wym')
        elif record['koniec'] and not re.match('^\d{2}:\d{2}$', str(record['koniec'])):
            push_to_to_correct(x, 'wym')


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

# for key in lecturers:
#     print(key)
#     print(lecturers[key])
