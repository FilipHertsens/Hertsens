import DB
import telepot
import keyboard as kb
from telepot.namedtuple import InlineKeyboardMarkup

api = "898207689:AAHNWFB3jlPdqG6sU-x8M4OgRWkE_GpTxGk"
admin = 953781362
bot = telepot.Bot(api)


def send_new_user(user):
    afdelingen = DB.get_afdelingen()
    but = []
    for afdeling in afdelingen:
        afdel = {}
        afdel[afdeling['naam']] = str(user['id'])+'_add_afdeling_'+afdeling['naam']
        but.append(afdel)
    end = {'Weigeren': str(user['id'])+'_add_afdeling_weigeren','Del msg': 'Del_msg'}
    but.append(end)
    end = {'Laat gebruiker het weten': 'startgebruiker_%s' % (str(user['id']))}
    but.append(end)
    bot.sendMessage(chat_id=admin, text=user['naam'] + '_'+ str(user['id']) + ' '+ 'wilt graag toegang.\nTot welke afdelingen wilt u hem toegang verlenen?',
                           reply_markup=InlineKeyboardMarkup(inline_keyboard=kb.Set_InlineKeyboard(but)))



def send_toelating(afdeling1,id):
    user = DB.get_user(str(id))
    afdelingen = DB.get_afdelingen()
    but = []

    for afdeling in afdelingen:
        if afdeling['naam'] == afdeling1:
            if 'toegangen' in afdeling:
                toegangen = afdeling['toegangen']
                for toegang in toegangen:

                    afdel = {}
                    afdel[toegang] = str(id) + '_add_afdelingtoelating_' + afdeling1+'_'+toegang
                    but.append(afdel)
                end = {'Del msg': 'Del_msg'}
                but.append(end)

            bot.sendMessage(chat_id=admin, text='%s_%s\n Welke toelating wilt u geven van de afdeling %s'
                                                % (user['naam'], str(id), afdeling1),
                            reply_markup=InlineKeyboardMarkup(inline_keyboard=kb.Set_InlineKeyboard(but)))
            return

    return False






if __name__ == '__main__':
    None