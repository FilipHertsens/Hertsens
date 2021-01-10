from telepot.namedtuple import InlineKeyboardButton

def Set_InlineKeyboard(rows):
    if not rows:
        return None
    else:
        buttons = []
        for row in rows:
            rowbuttons = []
            for text, call in row.items():
                rowbuttons.append(InlineKeyboardButton(text=text, callback_data=call))
            buttons.append(rowbuttons)
        return buttons
