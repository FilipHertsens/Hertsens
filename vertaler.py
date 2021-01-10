import csv
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(THIS_FOLDER, 'data/vertalingen.csv')


vertalinglijst = []

with open(filename) as fh:
    rd = csv.DictReader(fh, delimiter=';')
    for row in rd:
        vertalinglijst.append(row)

def vertaal(text, user=None):
    return text
    '''if user == None:
        taal = 'en'
    else:
        taal = user['taalcode']
    result1 = [x for x in vertalinglijst if x['nl'] == text]
    if len(result1) > 0:
        try:
            result = result1[0][taal]
            if result == '':
                return result1[0]['nl']
            else:
                return result1[0][taal]
        except:
            return result1[0]['nl']
    else:
        add_to_translatlist(text)
        return text'''

def add_to_translatlist(text):
    vertalinglijst.append({'nl': text})
    field_names = vertalinglijst[0].keys()

    with open(filename, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names, delimiter=';')
        writer.writeheader()
        writer.writerows(vertalinglijst)
