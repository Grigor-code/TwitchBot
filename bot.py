import config
import utils
import socket
import re
import time
import _thread
from time import sleep


def main():
    s = socket.socket()
    s.connect((config.HOST, config.PORT))
    s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(config.CHAN).encode("utf-8"))



    chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    utils.mess(s, "Ⓘ Данное сообщение доступно только людям с маленьким Cock  ")
    utils.mess(s, "VoHiYo Для просмотра команд напишите !помощь  ")
    _thread.start_new_thread(utils.fillOpList, ())
    while True:
        response = s.recv(1024).decode("utf-8")

        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+", response)
            message = chat_message.sub("", response)


            print(response)
            if message.strip() == "!time":
                utils.mess(s, "Сейчас: " + time.strftime("%I:%M %p %Z on %A %B %d %Y"))
            if message.strip() == "!messages" and utils.isOp(username):
                utils.mess(s, "Do something awesome!")
                utils.mess(s, "AAAAAAAAAAAAAAAAAaaAAAAAAAAAAAAAAAAAAAAAAAAAA")
            if message.strip() == "!ярик":
                utils.mess(s,"осуждаю!осуждаю!осуждаю!осуждаю!осуждаю!осуждаю!осуждаю!осуждаю!осуждаю!осуждаю!осуждаю!")
            if message.strip().split()[0] == "!gpt":
                new_string = ' '.join( message.strip().split()[1:])
                utils.chatGTP(s, new_string)
            if message.strip() == "!дискорд":
                utils.mess(s,"TwitchUnity  https://discord.gg/3tUpP9Jxf TwitchUnity ")
            if message.strip() == "!помощь":
                utils.mess(s,"!помощь : список команд //работает")
                utils.mess(s,"!gpt + сообщение: запрос для чат-гпт //работает")
                utils.mess(s, "!дискорд : получение ссылки для дискорда //работает")
                utils.mess(s, "!дота : дота id")
                utils.mess(s, "!рулетка : испытать удачу")
                utils.mess(s, "!ролл : разборки мужиков")
                utils.mess(s, "!герой : н**уй рандом в доте")
            if message.strip()=="!чистка" and utils.isOp(username):
                utils.mess(s,".clear")
            if message.strip() == "!дота":
                utils.mess(s,"добавляйтесь и кидайте репорты 179032894")
            if message.strip() == "привет":
                utils.mess(s, "Привет, это я - твой единственный зритель")
            if message.strip() == "!ролл":
                utils.roll(s,username)
            if message.strip() == "!рулетка":
                utils.radom(s,username)
                print(username)
            if message.strip() == "!герой":
                utils.randomhero(s,username)

        sleep(1)

if __name__ == "__main__":
    main()
