import config
import utils
import socket
import re
import time
import _thread
from time import sleep
import PySimpleGUI as sg

s=None
commands = []

def handle_commands(command, username):
    if command.startswith('!'):
        if command == "!time":
            utils.mess(s, "Сейчас: " + time.strftime("%I:%M %p %Z on %A %B %d %Y"))
        elif command == "!messages" and utils.isOp(username):
            utils.mess(s, "Do something awesome!")
            utils.mess(s, "AAAAAAAAAAAAAAAAAaaAAAAAAAAAAAAAAAAAAAAAAAAAA")
        elif command == "!ярик":
            utils.mess(s, "осуждаю!осуждаю!осуждаю!осуждаю!осуждаю!осуждаю!осуждаю!осуждаю!осуждаю!осуждаю!осуждаю!")
        elif command.startswith("!gpt "):
            new_string = command[5:]
            utils.chatGTP(s, new_string)
        elif command == "!дискорд":
            utils.mess(s, "TwitchUnity  https://discord.gg/3tUpP9Jxf TwitchUnity ")
        elif command == "!помощь":
            utils.mess(s, "!помощь: список команд")
            utils.mess(s, "!gpt + сообщение: запрос для чат-гпт ")
            utils.mess(s, "!дискорд: получение ссылки для дискорда ")
            utils.mess(s, "!дота: дота id")
            utils.mess(s, "!рулетка: испытать удачу")
            utils.mess(s, "!ролл: разборки мужиков")
            utils.mess(s, "!герой: н**уй рандом в доте")
        elif command == "!чистка" and utils.isOp(username):
            utils.mess(s, ".clear")
        elif command == "!дота":
            utils.mess(s, "добавляйтесь и кидайте репорты 179032894")
        elif command == "привет":
            utils.mess(s, "Привет, это я - твой единственный зритель")
        elif command == "!ролл":
            utils.roll(s, username)
        elif command == "!рулетка":
            utils.radom(s, username)

        elif command == "!герой":
            utils.randomhero(s, username)
        else:
            # Check if the command is in the custom commands list
            for custom_command, custom_message in commands:
                if command == custom_command:
                    utils.mess(s, custom_message)
                    break
            else:
                utils.mess(s, "Unknown command: " + command)



def main():
    global s
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
            if message.startswith('!'):
                handle_commands(message.strip(), username)

        sleep(1)

layout = [
    [sg.Multiline(size=(80, 20), key='-OUTPUT-', reroute_stdout=True)],
    [sg.Input(key='-COMMAND-'), sg.Input(key='-MESSAGE-'), sg.Button('Добавить команду')],
    [sg.Input(key='-INPUT-'),sg.Button('Вывести', bind_return_key=True),sg.Button('Закрыть')]
]
window = sg.Window("Бот пиздабол", layout)

_thread.start_new_thread(main, ())
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Закрыть':
        utils.mess(s, "Всем пока!")
        break
    elif event == 'Вывести':
        text = values['-INPUT-']
        utils.mess(s, text)
        window['-INPUT-'].update('')


window.close()
