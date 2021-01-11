print('[START SCRIPT]')

import mail
import telegram
import time
import DB
import WacsClient
from threading import Thread

api = "898207689:AAHNWFB3jlPdqG6sU-x8M4OgRWkE_GpTxGk"
admin = 953781362


if __name__ == "__main__":
    telegram.MessageLoop(telegram.bot, {'chat': telegram.on_chat_message,
                                        'callback_query': telegram.on_callback_query}).run_as_thread()
    while 1:
        thread = Thread(target=WacsClient.update_list_voertuigen, args=(1800,))
        thread.start()
        thread.join()
        time.sleep(1800)



print('[START TELEPOT LOOP]')
while 1:
    time.sleep(1)