import telepot
import time
from datetime import datetime
from pprint import pprint
from telepot.loop import MessageLoop
import DB
import teleadmin
import sendmessages as sm
from vertaler import vertaal
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove, ForceReply
#import geolocatie

api = "898207689:AAHNWFB3jlPdqG6sU-x8M4OgRWkE_GpTxGk"
admin = 953781362
bot = telepot.Bot(api)


def delete_msg(id, msgid):
    try:
        bot.deleteMessage(msg_identifier=(id, msgid))
    except:
        pass


def on_chat_message(msg):
    pprint(msg)
    content_type, chat_type, chat_id = telepot.glance(msg)
    user = DB.get_user(str(chat_id))
    delete_msg(chat_id, msg['message_id'])
    if not user:
        user = DB.add_user(msg)

    if 'location' in msg:
        if user['nu_toelating'] == 'Tijdsregistratie':
            sm.send_tijdsregistratie_locatie(user=user, locatie=msg['location'])
            print ('%-25s%-25s%-60s%-20s' % ('[LOCATIE]', user['naam'], 'locatie ontvangen', sm.get_time()))

    elif 'text' in msg:
        tx = msg['text']
        text = '[BERICHT]'
        print ('%-25s%-25s%-60s%-20s' % (text, user['naam'], tx, sm.get_time()))
        if tx[0] == '/':
            if tx == '/start':
                if 'afdelingen' in user:
                    idd = user['id']
                    sm.send_new_start(id=idd)
                else:
                    bericht = bot.sendMessage(chat_id=chat_id, text=vertaal(
                        text='We hebben een toegangsaanvraag voor jou verstuurd.', user=user))
                    DB.add_user_data(chat_id, 'last_msg_id', bericht['message_id'])
                    teleadmin.send_new_user(user)

        elif 'afdeling' in user:
            if 'nu_toelating' in user:
                toelating = user['nu_toelating']
                if toelating not in ['Tijdsregistratie']:
                    sm.send_lijstvoertuigen(user=user, text=tx)
                else:
                    sm.send_tijdsregistratie_opmerking(user, tx)

        else:
            bericht = bot.sendMessage(chat_id=chat_id, text=vertaal(
                text='We hebben een toegangsaanvraag voor jouw verstuurd.', user=user))
            DB.add_user_data(chat_id, 'last_msg_id', bericht['message_id'])
            teleadmin.send_new_user(user)


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    user = DB.get_user(str(from_id))

    text = '[BUTTON]'
    print('%-25s%-25s%-60s%-20s' % (text, user['naam'], msg['data'], sm.get_time()))

    if '_Vgnr_' in query_data:
        nr = query_data.split('_Vgnr_')[1]
        DB.add_user_data(user['id'], 'nu_voertuig', nr)

    if 'Del_msg' in query_data:
        delete_msg(from_id, msg['message']['message_id'])

    elif '_add_afdeling_weigeren' in query_data:
        idd = int(query_data.split('_')[0])
        bot.sendMessage(chat_id=idd, text=vertaal(text='Je krijgt geen extra toegang', user=idd))
        delete_msg(from_id, msg['message']['message_id'])

    elif '_add_afdeling_' in query_data:
        idd = int(query_data.split('_')[0])
        afdeling = query_data.split('_')[3]
        teleadmin.send_toelating(afdeling1=afdeling, id=idd)

    elif '_add_afdelingtoelating_' in query_data:
        idd = int(query_data.split('_')[0])
        afdeling = query_data.split('_')[3]
        toelating = query_data.split('_')[4]
        DB.add_user_toelating(idd, afdeling, toelating)

    elif 'startgebruiker_' in query_data:
        idd = int(query_data.split('_')[1])
        sm.send_start(id=idd)

    elif '_open_afdeling_' in query_data:
        idd = int(query_data.split('_')[0])
        afdeling = query_data.split('_')[3]
        sm.send_afdeling(id=idd, afdeling=afdeling)
        DB.add_user_data(user['id'], 'nu_afdeling', afdeling)

    elif '_terug_naar_afdelingen' in query_data:
        idd = int(query_data.split('_')[0])
        sm.send_start(id=idd)
        DB.add_user_data(user['id'], 'nu_afdeling', '')
        DB.add_user_data(user['id'], 'nu_toelating', '')
        DB.add_user_data(user['id'], 'nu_voertuig', '')



    elif '_terug_naar_toelatingen_' in query_data:
        idd = int(query_data.split('_')[0])
        afdeling = query_data.split('_')[4]
        sm.send_afdeling(id=idd, afdeling=afdeling)
        DB.add_user_data(user['id'], 'nu_afdeling', afdeling)
        DB.add_user_data(user['id'], 'nu_toelating', '')
        DB.add_user_data(user['id'], 'last_tijdregistratie_id', '')
        DB.add_user_data(user['id'], 'nu_voertuig', '')
        if 'last_tijdregistratie_id' in user:
            if user['last_tijdregistratie_id'] != '':
                delete_msg(idd,user['last_tijdregistratie_id'])


    elif '_instellingen_user' in query_data:
        idd = int(query_data.split('_')[0])
        sm.send_instellingen_user(id=idd)

    elif '_meer_toegangen' in query_data:
        idd = int(query_data.split('_')[0])
        user = DB.get_user(str(idd))
        teleadmin.send_new_user(user)


    elif '_open_toegang_' in query_data:
        idd = int(query_data.split('_')[0])
        afdeling = query_data.split('_')[3]
        toelating = query_data.split('_')[4]
        sm.send_toelating(id=idd, afdeling=afdeling, toelating=toelating)

    elif '_Vgnr_' in query_data:
        idd = int(query_data.split('_')[0])
        infoset = query_data.split('_')[1]
        sm.send_asset_info(idd=idd, infoset=infoset)

    else:
        idd = user['id']
        sm.send_start(id=idd)


if __name__ == '__main__':
    MessageLoop(bot, {'chat': on_chat_message, 'callback_query': on_callback_query}).run_as_thread()
    print('[START TELEPOT LOOP]')
    while 1:
        time.sleep(1)
