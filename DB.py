import json
import arrow
from pprint import pprint
import vertaler
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
pathusers = os.path.join(THIS_FOLDER, 'data/gebruikers.json')
pathafdelingen = os.path.join(THIS_FOLDER, 'data/afdelingen.json')
pathuurregistraties = os.path.join(THIS_FOLDER, 'data/uurregistraties.json')





def get_uurregistraties(user=None):
    with open(pathuurregistraties, 'r') as json_file:
        data = json.load(json_file)
    if user == None:
        return data
    else:
        try:
            idd = user['id']
            result = [x for x in data if x['userid'] == idd and x['afdeling'] == user['nu_afdeling']
                      and x['actie'] in ['start','stop']]
            return result
        except:
            return []

def get_nritemuurregistraties(aantalitems=1,user=None):
    with open(pathuurregistraties, 'r') as json_file:
        data = json.load(json_file)
    if user == None:
        return data
    else:
        idd = user['id']
        result = [x for x in data if x['userid'] == idd and x['afdeling'] == user['nu_afdeling']]
        result = (sorted(result, key=lambda i: i['time'], reverse=True))
        result = result[:aantalitems]
        result = (sorted(result, key=lambda i: i['time'], reverse=False))
        return result


def add_uurregistraties(time=None,locatie=None,actie='',afdeling=None,idd=None,adres=None,opmerking=None):

    user = get_user(str(idd))
    reg = get_uurregistraties()
    item = {}
    item['adres'] = adres
    item['userid'] = idd
    item['time'] = time
    item['locatie'] = locatie
    item['actie'] = actie
    item['afdeling'] = afdeling
    item['opmerking'] = opmerking
    text = '[UURREGISTRATIE]'
    print ('%-25s%-25s%-25s%-35s%-20s' % (text,user["naam"],item['actie'],afdeling,item['time']))
    reg.append(item)
    return save_uurregistraties(reg)


def get_afdelingen():
    with open(pathafdelingen, 'r') as json_file:
        data = json.load(json_file)
    return data

def get_user(id):
    with open(pathusers, 'r') as json_file:
        users = json.load(json_file)
    return users[str(id)]


def get_users():
    with open(pathusers, 'r') as json_file:
        users = json.load(json_file)
    return users

def add_user_data(userid,field,data):
    userid = str(userid)
    users = get_users()
    try:
        users[userid][field] = data
        text = '[FIELD UPDATE USER]'
        print ('%-25s%-25s%-25s%-20s' % (text,users[userid]["naam"],str(field),str(data)))
        return save_users(users)
    except:
        return False

def add_user_toelating(userid,field,data):
    userid = str(userid)
    users = get_users()
    if 'afdeling' in users[userid]:
        None
    else:
        users[userid]['afdeling'] = {}
    if field not in users[userid]['afdeling']:
        users[userid]['afdeling'][field] = []
    if data not in users[userid]['afdeling'][field]:
        users[userid]['afdeling'][field].append(data)

    text = '[TOELATING UPDATE]'
    print ('%-25s%-25s%-20s%-20s' % (text,users[userid]["naam"],str(field),str(data)))
    return save_users(users)





def save_users(users):
    try:
        with open(pathusers, 'w') as outfile:
            json.dump(users, outfile, indent=4)
        return True
    except:
        return False

def save_uurregistraties(registraties):
    try:
        with open(pathuurregistraties, 'w') as outfile:
            json.dump(registraties, outfile, indent=4)
        return True
    except:
        return False


def get_user(userid):
    users = get_users()
    if userid in users:
        user = users[userid]
        return user
    else:
        return False


def add_user(msg):
    users = get_users()
    user = {}
    user['id'] = msg['chat']['id']
    user['taalcode'] = msg['from']['language_code']
    voornaam = ''
    achternaam = ''
    if 'first_name' in msg['chat']:
        voornaam = msg['chat']['first_name']
    if 'last_name' in msg['chat']:
        achternaam = msg['chat']['last_name']
    user['naam'] = voornaam + ' ' + achternaam
    users[user['id']] = user
    print ('[ADD USER]\t\t %s' %user["naam"])
    save_users(users)
    return user

def get_newest_tijdsregistratie(result):
    if len(result) == 0:
        return False
    else:
        result = (sorted(result, key=lambda i: i['time'],reverse=True))
        return result[0]

def nexxt_uurregistratie(user):
    result = get_uurregistraties(user=user)
    result1 = get_newest_tijdsregistratie(result)
    if result1:
        last_actie = result1['actie']
        if last_actie in ['start']:
            textbutton = 'stop'
        else:
            textbutton = 'start'
    else:
        textbutton = 'start'
    return textbutton

def today_uurregistratie(user):
    bericht = ''
    registraties = get_nritemuurregistraties(aantalitems=7, user=user)
    pprint(registraties)
    for reg in registraties:
        if reg['actie'] == 'opmerking':
            bericht += '\n'+vertaler.vertaal(text='Opmerking',user=user)+': '+reg['time']+'\n      '+reg['opmerking']
        else:
            bericht += '\n'+vertaler.vertaal(text=reg['actie'],user=user) + ': ' + reg['time']+'\n'
    if bericht == '':
        bericht = vertaler.vertaal(text='Tijdsregistratie',user=user)
    return bericht



