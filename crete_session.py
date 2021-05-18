import os
from random import choice
from telethon.errors import PhoneNumberBannedError
from telethon import TelegramClient
phones = open('phones.txt').read().split('\n')
apis = open('apis.txt',encoding='utf-8').read().split('\n')
i = 0
z = 0
for phone in phones:
    i+=1
    print(phone +' '+str(i)+'|'+str(len(phones)))
    api = choice(apis).split(' ')
    client = TelegramClient(phone, int(api[0]), api[1])
    try:
        client.start(phone=phone)
    except PhoneNumberBannedError:
        client.disconnect()
        z+=1
        os.remove(phone+'.session')
        continue
    except:
        z+=1
        client.disconnect()
        try:
            os.remove(phone + '.session')
        except:
            pass
        continue
    client.disconnect()
input(f'ban {z}')