import DB
import telepot
import telegram
import keyboard as kb
from vertaler import vertaal
import WacsClient
from datetime import datetime, date
from telepot.namedtuple import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import teleadmin
from pprint import pprint
#import geolocatie




api = "1458391973:AAEOd4ToPFK2bmCzblPGIc5YovTOp05-gNM"
admin = 953781362
bot = telepot.Bot(api)

def get_time(x=None):
    if x == None:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        today = date.today()
        d1 = today.strftime("%d/%m/%Y ")
        return d1 + current_time
    else:
        return 'nog niet geprogrammeerd'

def send_msg(text,user,but=[]):
    try: bot.editMessageText(text=vertaal(text=text,user=user),msg_identifier=(user['id'],user['last_msg_id']),
                             reply_markup=InlineKeyboardMarkup(inline_keyboard=kb.Set_InlineKeyboard(but)))
    except:
        bericht = bot.sendMessage(chat_id=user['id'], text=vertaal(text=text,user=user),
                                  reply_markup=InlineKeyboardMarkup(inline_keyboard=kb.Set_InlineKeyboard(but)))
        DB.add_user_data(user['id'], 'last_msg_id', bericht['message_id'])

def send_msg_location(text,user):
    textbutton = DB.nexxt_uurregistratie(user)+' werkdag'

    try:
        telegram.delete_msg(user['id'], user['last_tijdregistratie_id'])
    except:
        None
    bericht = bot.sendMessage(text=text,chat_id=user['id'],
                    reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(
                        text=vertaal(textbutton,user), request_location=True)]]))
    DB.add_user_data(user['id'], 'last_tijdregistratie_id', bericht['message_id'])


def send_new_start(id):
    but = []
    user = DB.get_user(str(id))
    afdelingen = user['afdeling']
    for afdeling,toelating in afdelingen.items():
        afdel = {}
        afdel[vertaal(afdeling,user)] = str(id)+'_open_afdeling_' + afdeling
        but.append(afdel)
    BNinstellingen = {'<<< '+vertaal('Instellingen', user): str(id) + '_instellingen_user'}
    but.append(BNinstellingen)
    bericht = bot.sendMessage(chat_id=user['id'], text=vertaal(text='Kies een afdeling:', user=user),
                              reply_markup=InlineKeyboardMarkup(inline_keyboard=kb.Set_InlineKeyboard(but)))
    DB.add_user_data(user['id'], 'last_msg_id', bericht['message_id'])

def send_start(id):
    but = []
    user = DB.get_user(str(id))
    afdelingen = user['afdeling']
    for afdeling,toelating in afdelingen.items():
        afdel = {}
        afdel[vertaal(afdeling,user)] = str(id)+'_open_afdeling_' + afdeling
        but.append(afdel)
    BNinstellingen = {'<<< '+vertaal('Instellingen', user): str(id) + '_instellingen_user'}
    but.append(BNinstellingen)
    send_msg(text='Kies een afdeling:', user=user, but=but)


def send_afdeling(id,afdeling):
    but = []
    user = DB.get_user(str(id))
    toegangen = user['afdeling'][afdeling]

    if (len(toegangen) % 2) == 0:
        for x, y in grouped(toegangen, 2):
            afdel = {}
            afdel[vertaal(x, user)] = str(id) + '_open_toegang_' + afdeling + '_' + x
            afdel[vertaal(y, user)] = str(id) + '_open_toegang_' + afdeling + '_' + y
            but.append(afdel)
        BNterug = {'<<< ' + vertaal('Terug', user): str(id) + '_terug_naar_afdelingen'}
        but.append(BNterug)
    else:
        for x, y in grouped(toegangen[:-1], 2):
            afdel = {}
            afdel[vertaal(x, user)] = str(id) + '_open_toegang_' + afdeling + '_' + x
            afdel[vertaal(y, user)] = str(id) + '_open_toegang_' + afdeling + '_' + y
            but.append(afdel)
        last= {}
        last['<<< ' + vertaal('Terug', user)] = str(id) + '_terug_naar_afdelingen'
        last[vertaal(toegangen[-1], user)] = str(id) + '_open_toegang_' + afdeling + '_' + toegangen[-1]
        but.append(last)
    send_msg('Wat wil je doen?', user, but)


def send_toelating(id, afdeling, toelating,msg=None):
    user = DB.get_user(str(id))
    but = []
    BNterug = {'<<< '+vertaal('Terug', user): str(id) + '_terug_naar_toelatingen_'+afdeling}

    DB.add_user_data(user['id'], 'nu_afdeling', afdeling)
    DB.add_user_data(user['id'], 'nu_toelating', toelating)
    if toelating in ['Voertuiglocatie','Herstelaanvraag','Bandendrukken','Voertuiginfo'] and user['nu_voertuig'] == '':
        but.append(BNterug)
        send_msg('Wat is de nummer of nummerplaat van de machine?', user, but)
    elif toelating in ['Tijdsregistratie']:
        but.append(BNterug)
        send_msg('Welkom bij de tijdsregistratie-module\n\nTelkens je op de knop [start dag] of [einde dag] klikt gaan we ook naar je huidige locatie vragen.\nVoor een opmerking stuur je me nu een berichtje.', user, but)
        bericht = DB.today_uurregistratie(user)
        send_msg_location(text=bericht,user=user)

    else:
        send_asset_info(id, toelating)


def send_lijstvoertuigen(user,text):
    but = []
    afdeling = user['nu_afdeling']
    if afdeling == '':
        return False
    afdelingen = DB.get_afdelingen()
    types = [x for x in afdelingen if x['naam'] == afdeling][0]['header1']
    voertuigen = WacsClient.GetListVoertuigen()

    if len(text) < 4:
        while len(text) < 3:
            text = '0'+text
        zoekcriteria = 'Name'
        result = [x for x in voertuigen if x['Active'] and x['Type'].upper() in types and text in x[zoekcriteria]]
    else:
        zoekcriteria = 'Header1'
        result1 = [x for x in voertuigen if x['Active'] and x['Type'].upper() in types]
        result = []
        for x in result1:
            if x[zoekcriteria] != None:
                if text.upper() in x[zoekcriteria]:
                    result.append(x)
    if len(result):
        bericht = 'Kies jouw voertuig.'
        if len(result) > 15:
            bericht = 'Je imput was niet specifiek genoeg.'
        else:
            for asset in result:
                name = asset['Name'].split(' ')[0]
                buttonname = vertaal(asset['Type'],user)+' '+name+' '+asset['Header1']
                afdel = {}
                afdel[buttonname] = str(user['id']) + '_' + user['nu_toelating'] + '_Vgnr_' + name
                but.append(afdel)
    else:
        bericht = 'Geen voertuigen gevonden'

    BNterug = {'<<<' +vertaal('Terug', user): str(user['id']) + '_terug_naar_toelatingen_' + user['nu_afdeling']}
    but.append(BNterug)
    send_msg(bericht, user, but)

def send_instellingen_user(id):
    user = DB.get_user(str(id))
    but = []
    BNmorpremission = {vertaal('Vraag meer toegangen',user): str(user['id']) + '_meer_toegangen'}
    but.append(BNmorpremission)
    BNterug = {'<<< ' + vertaal('Terug', user): str(id) + '_terug_naar_afdelingen'}
    but.append(BNterug)
    send_msg('Instellingen', user, but)

def send_asset_info(idd,infoset):
    but = []
    user = DB.get_user(str(idd))
    toegangen = user['afdeling'][user['nu_afdeling']]
    if user['nu_toelating'] in toegangen: toegangen.remove(user['nu_toelating'])
    if 'Tijdsregistratie' in toegangen: toegangen.remove('Tijdsregistratie')
    if (len(toegangen) % 2) == 0:
        for x, y in grouped(toegangen, 2):
            afdel = {}
            afdel[vertaal(x, user)] = str(user['id']) + '_open_toegang_' + user['nu_afdeling']+'_' + x + \
                                '_Vgnr_' + user['nu_voertuig']
            afdel[vertaal(y, user)] = str(user['id']) + '_open_toegang_' + user['nu_afdeling']+'_' + y + \
                                '_Vgnr_' + user['nu_voertuig']
            but.append(afdel)
        BNterug = {'<<< ' + vertaal('Terug', user): str(idd) + '_terug_naar_afdelingen'}
        but.append(BNterug)
    else:
        for x, y in grouped(toegangen[:-1], 2):
            afdel = {}
            afdel[vertaal(x, user)] = str(user['id']) + '_open_toegang_' + user['nu_afdeling']+'_' + x + \
                                '_Vgnr_' + user['nu_voertuig']
            afdel[vertaal(y, user)] = str(user['id']) + '_open_toegang_' + user['nu_afdeling']+'_' + y + \
                                '_Vgnr_' + user['nu_voertuig']
            but.append(afdel)
        last = {}
        last['<<< ' + vertaal('Terug', user)] = str(idd) + '_terug_naar_afdelingen'
        last[vertaal(toegangen[-1], user)] = str(idd) + '_open_toegang_' + user['nu_afdeling'] + '_' + toegangen[-1]
        but.append(last)

    bericht= infoset
    send_msg(vertaal(bericht,user)+' : '+user['nu_voertuig'], user, but)

def send_tijdsregistratie_locatie(user, locatie):
    #adres = geolocatie.InPoly(locatie)
    adres = 'adres'
    actie = DB.nexxt_uurregistratie(user)
    DB.add_uurregistraties(time=get_time(), locatie=locatie, actie=actie, afdeling=user['nu_afdeling'],
                           idd=user['id'], adres=adres)
    bericht = DB.today_uurregistratie(user)
    send_msg_location(bericht, user)

def send_tijdsregistratie_opmerking(user, opmerking):
    DB.add_uurregistraties(time=get_time(), actie='opmerking', afdeling=user['nu_afdeling'],
                           idd=user['id'], opmerking=opmerking)
    bericht = DB.today_uurregistratie(user)
    send_msg_location(bericht, user)


def grouped(iterable, n):
    return zip(*[iter(iterable)]*n)