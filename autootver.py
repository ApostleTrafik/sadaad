from telethon import events
import asyncio
import os
from random import uniform, choice
import random
from time import sleep

import requests
import socks
from bs4 import BeautifulSoup
from telethon import TelegramClient
from telethon.errors import PhoneNumberBannedError, FloodWaitError
from concurrent.futures import ThreadPoolExecutor as PoolExecutor

from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import InputPeerChannel
def start(data):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    global block,group_
    sleep(uniform(1,5))
    groups = data[1]
    client = TelegramClient(data[0][0], data[0][1], data[0][2])
    try:
        client.start(phone=phone)
    except PhoneNumberBannedError:
        client.disconnect()
        os.remove(phone + '.session')
        print(phone+' ban')
        while True:
            pass

    async def main():
        global group_
        group_ = await client.get_entity(group_)
    with client:
        client.loop.run_until_complete(main())
    groups_ids = []
    for group in groups:
        print(group)
        async def main():
            try:
                await client(JoinChannelRequest(group))
            except FloodWaitError as e:
                print(f'{data[0][0]} sleep {e.seconds}')
                sleep(e.seconds)
                await client(JoinChannelRequest(group))
            except:
                try:
                    await client(ImportChatInviteRequest(group.split('/')[-1]))
                except FloodWaitError as e:
                    print(f'{data[0][0]} sleep {e.seconds}')
                    sleep(e.seconds)
                except:
                    print(f'----- {phone}-----{group}')
            try:
                ids  = await client.get_entity(group)
                groups_ids.append(ids.id)
            except:
                pass
        with client:
            client.loop.run_until_complete(main())
        sleep(uniform(10,15))
    @client.on(events.NewMessage())
    async def handler(event):
        try:
            username = await client.get_entity(event.from_id)
            if int(str(event.message.peer_id).split('=')[1].split(')')[
                       0]) in groups_ids and username.username not in block:
                await client.forward_messages(messages=event.message, entity=group_)
        except:
            try:
                if int(str(event.message.peer_id).split('=')[1].split(')')[
                           0]) in groups_ids :
                    await client.forward_messages(messages=event.message, entity=group_)
            except:
                pass
    with client:
        print(f'{data[0][0]} start')
        client.run_until_disconnected()
if __name__ == '__main__':
    group_ = input('Group:\n')
    apis = open('apis.txt',encoding='utf-8').read().split('\n')
    phones_ = open('phones.txt',encoding='utf-8').read().split('\n')
    groups_ = set(open('groups.txt',encoding='utf-8').read().split('\n'))
    print(len(groups_))
    groups = []
    for grou in groups_:
        groups.append(grou)
    block = open('blocks.txt').read().split('\n')
    phones = []
    for phone in phones_:
        if phone == '':
            continue
        print(phone)
        api = choice(apis).split(' ')
        client = TelegramClient(phone, int(api[0]), api[1])
        try:
            client.start(phone=phone)
        except PhoneNumberBannedError:
            client.disconnect()
            os.remove(phone + '.session')
            continue
        async def main():
            try:
                await client(ImportChatInviteRequest(group_.split('/')[-1]))
            except:
                try:
                    await client(JoinChannelRequest(group_))
                except:
                    pass
        with client:
            client.loop.run_until_complete(main())
        client.disconnect()
        phones.append([phone, int(api[0]), api[1]])
    list_ = []
    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            list_.append(lst[i:i + n])
    n = len(groups) // len(phones)
    chunks(groups,n)
    procs = []
    for i in range(len(list_)):
        try:
            procs.append([phones[i],list_[i]])
        except:
            pass
    with PoolExecutor(max_workers=len(list_)) as executor:
        for _ in executor.map(start, procs):
            pass