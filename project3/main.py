import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import sys

# to_correct is a hash consisting of records, which data is to be corrected
# its values are the wrong records and keys - row:column

to_correct = []
lecturers = {}
overlapping = []


def load_from_spreadsheet(key_file, spreadsheet_name):
    # connect to the spreadsheet

    scope = ['http://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(key_file, scope)

    gc = gspread.authorize(credentials)

    return gc.open(spreadsheet_name).sheet1.get_all_records()


def print_lecturers_classes(data):
    print('Lecturers classes:')
    for key in data:
        print(key)
        for lecture in data[key]:
            print(lecture)
        print('\n')


def print_overlapping_classes(data):
    print('Overlapping classes:')
    for record in data:
        print(record['record'])
        print(record['record2'])
        print('\n')


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
    to_correct.append(new_obj)


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

        if not record['typ'] or not record['przedmiot']:
            push_to_to_correct(x, 'blank')
        elif not re.match('^s\d+$', record['studia']):
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


def check_overlapping(arr):
    for x in arr:
        record = x['record']

        for y in arr:
            record2 = y['record']

            if record != record2 and record['studia'] == record2['studia'] and record['sem'] == record2['sem'] \
                    and record['pora'] == record2['pora'] and record['miejsce'] == record2['miejsce'] \
                    and record['godz'] == record2['godz'] and record['tyg'] == record2['tyg'] \
                    and record['dzien'] == record2['dzien']:
                new_obj = {}
                new_obj['record'] = record
                new_obj['record2'] = record2
                overlapping.append(new_obj)


def main():
    if len(sys.argv) == 2:
        # open the spreadsheet

        wks = load_from_spreadsheet(sys.argv[1], 'MendrochPythonProject3')

        # process the spreadsheet

        wks = filter_records(wks)

        correct_arr(wks)

        check_overlapping(wks)

        while 1:
            print('____________________________________________________________________')
            print('c - lines to correct, l - lecturers classes, r - overlapping classes')
            print('\n')

            try:
                line = sys.stdin.readline()

                if line[:-1] == 'c':
                    print('Lines to correct:')
                    for i in to_correct:
                        print(i)
                elif line[:-1] == 'l':
                    print_lecturers_classes(lecturers)
                elif line[:-1] == 'r':
                    print_overlapping_classes(overlapping)

            except KeyboardInterrupt:
                break

            if not line:
                break

    else:
        print('Please provide the filename with json key at argv[1]')


main()
