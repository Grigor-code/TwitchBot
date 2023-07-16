import config
import urllib.request
import json
from time import sleep
import openai


import random


openai.api_key=config.TOKEN
engine="text-davinci-003"

def chatGTP(sock,message):
    completion = openai.Completion.create(engine=engine,
                                          prompt=message,
                                          temperature=0.5,
                                          max_tokens=1000)
    string=str(completion.choices[0]['text'])
    no_dots_string = string.replace("\n", "")
    split_text = [no_dots_string[i:i + 255] for i in range(0, len(no_dots_string), 255)]

    for i in range (0,len(split_text)):
        mess(sock, split_text[i])




def mess(sock, message):
    msg = "PRIVMSG #" + config.CHAN + " :" + message + "\r\n"
    sock.send(msg.encode())
    print(msg)


def roll(sock, user):
    a=random.randint(1,100)
    if user:
        result = user.group()
    mess(sock, "@{}".format(result) + " заролил {}".format(a))

def ban(sock, user):
    mess(sock, ".ban {}".format(user))

def randomhero(sock,user):
    random_hero=random.choice(config.heroes)
    if user:
        result = user.group()
    mess(sock, "@{}".format(result) + " сегодня играет, например, на {}".format(random_hero))

def radom(sock, user):
    a=random.randint(1,5)
    if user:
        result = user.group()

    if a==1:
        mess(sock, "@{}".format(result) + " повезло, но почему рот в говне")


    else :
        mess(sock, "@{}".format(result) + " неудачник проебал жопу")
        






def timeout(sock, user, seconds = 500):
    command = f".timeout {user} {seconds}"
    mess(sock, command)


def caca(sock):
        mess(sock,"СТРИМ ЗАКОНЧЕН")



#req = request
#res = response
def fillOpList():
    while True:
        try:
            url = "http://tmi.twitch.tv/group/user/winderton/chatters"
            req = urllib.Request(url, headers={"accept": "*/*"})
            res = urllib.urlopen(req).read()
            if res.find("502 bad gateway") == - 1:
                config.oplist.clear()
                data = json.loads(res)
                for p in data["chatters"]["moderators"]:
                    config.oplist[p] = "mod"
                for p in data["chatters"]["global_mods"]:
                    config.oplist[p] = "global_mod"
                for p in data["chatters"]["admins"]:
                    config.oplist[p] = "admin"
                for p in data["chatters"]["staff"]:
                    config.oplist[p] = "staff"
        except:
            "Something went wrong...do nothing"
        sleep(5)
def isOp(user):
    return user in config.oplist

