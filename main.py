import datetime
import json
import os
import threading
import time
from random import randint

import vk_api

this_time = datetime.datetime.now()
dirname = str(this_time.strftime("%d-%m-%Y"))
filename = 'history_' + this_time.strftime("%d-%m-%Y_%H-%M") + '.log'

def log(text):
    if os.path.exists(dirname) :
        pass
    else:
        os.mkdir(dirname)
    if os.path.isfile(dirname + '/' + filename) :
        with open((dirname +'/' +filename), 'a') as f:
            f.write('[' +this_time.strftime("%d-%m-%Y %H:%M") +'] ' +text +'\n')
            f.close()
    else:
        with open((dirname +'/' +filename), 'w') as f:
            f.write('[' +this_time.strftime("%d-%m-%Y %H:%M") +'] ' +text+'\n')
            f.close()

def listen_user(id):
    while True:
        spuser = vk.users.get(user_ids=id, fields=more, name_case='nom')
        last_seen = int(spuser[0]['last_seen']['time'])
        last_seen = datetime.datetime.fromtimestamp(last_seen).strftime('%Y-%m-%d %H:%M:%S')
        online = spuser[0]['online']
        if(online == 1):
            online = ' онлайн.'
        else:
            online = ' оффлайн.'
        name = spuser[0]['first_name'] + ' ' +spuser[0]['last_name']
        time.sleep(randint(1,5))
        log(name +online)
        log('Пользователь ' +name +' последний раз заходил(а) в сеть ' + last_seen)
        log('-------------')
        time.sleep(30)

if(os.path.isfile('config.cfg')):
    with open("config.cfg", "r") as cfg:
        try:
            config = json.load(cfg)
            config = config[0]
        except BaseException as e:
            print(e)
            cfg.close()
            os.remove('config.cfg')
            exit()
        cfg.close()
else:
    with open('config.json', 'w') as cfg:
        json.dump([{
                            'ids': [],
                            'token': '',
                            'more': ['last_seen'],
                    }], cfg)
        cfg.close()

token = config['token']
ids = config['ids']
more = 'last_seen, online'

if(token == ''):
    log('Токен пустой')
    exit()
if(ids == []):
    log('Пустой список ID страниц')
    exit()
if(more == []):
    log('Список методов пуст. Обратитесь к разработчику.')
    exit()

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

for user in ids:
    threading.Thread(target=listen_user, args=(user, )).start()
    log('Запущено прослушивание для ID: ' + str(user))

log('-------------')
