#!/usr/bin/env python3
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from random import randint, choice
import requests
from os import remove
from glob import glob
from lib.memegenerator import make_meme
from time import sleep


def message(uid, msg):
    vk.messages.send(peer_id=uid, message=msg, random_id=randint(-2147483648, 2147483648))
    if DEBUG:
        print(message, "отправлено", uid)


def mark_read(uuid):
    retries = 0
    while retries <= 5:
        try:
            vk.messages.markAsRead(peer_id=uuid)
            break
        except:
            if DEBUG:
                print("could not send MarkAsRead packet, retrying")
            retries += 1
            sleep(2)


def make_photo(url, uuid, text):
    req = requests.get(url=url)
    extension = url[url.rfind("."):url.rfind("?")]
    if extension == ".jp":
        extension = ".jpg"
    try:
        download_file = open(images_folder + "img_received" + extension, "wb")
        download_file.write(req.content)
        download_file.close()
        # meme generator moment
        meme = make_meme(text[0], text[1], images_folder + "img_received" + extension)
        meme.save(images_folder + "img_output" + extension)
        upload = vk_api.VkUpload(vk)
        photo = upload.photo_messages(images_folder + "img_output" + extension)
    except:
        message(uuid, "Ой ох.... Что то пошло не так... Попробуйте отправить ещё разок...")
        return -1
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    vk.messages.send(peer_id=uuid, random_id=randint(-2147483648, 2147483648), attachment=attachment)
    tree = glob(images_folder + "*")
    for i in tree:
        remove(i)


if __name__ == "__main__":
    while True:
        try:
            try:
                print("reading configuration...")
                images_folder = "images/"
                KEY = None
                GROUPID = None
                DEBUG = True
                conf_file = open("config.cfg")
                conf_params = conf_file.read().split("\n")
                conf_file.close()
                for parameter in conf_params:
                    parameter = parameter.split("=")
                    if parameter[0] == "images_folder":
                        images_folder = parameter[1]
                        print("working folder=", images_folder, sep="")
                    elif parameter[0] == "token":
                        KEY = parameter[1]
                    elif parameter[0] == "groupid":
                        GROUPID = parameter[1]
                    elif parameter[0] == "DEBUG":
                        if parameter[1].lower() == "true":
                            DEBUG = True
                        else:
                            DEBUG = False
                        print("debug=", DEBUG, sep="")
            except IndexError:
                print("Could not read configuration. Visit github.com/Frog-Lover-Antony/vk-membot to get more info.")
                exit(-1)
            except FileNotFoundError:
                print("File config.conf does not seem to exist. Please, visit Frog-Lover-Antony/vk-membot "
                      "if you have any trouble running the script.")
                exit(-1)
            try:
                vk_session = vk_api.VkApi(token=KEY)
                vk = vk_session.get_api()
            except vk_api.AuthError:
                print("could not Authenticate!")
                exit(-1)
            if vk is None or vk_session is None:
                print("Something went wrong!", vk, vk_session)
                exit(-2)
            print("Authenticated!")
            if DEBUG:
                print("starting listener...")
            longpoll = VkBotLongPoll(vk_session, GROUPID)
            print("Listener started.")

            for event in longpoll.listen():
                if DEBUG:
                    print(event)
                msg = event.obj["text"].lower()
                uuid = event.obj["from_id"]
                mark_read(uuid)
                if event.type == VkBotEventType.MESSAGE_NEW and event.obj["attachments"]:
                    if event.obj["text"]:
                        text = [str(event.obj["text"]).split("\n")]
                        if len(text) > 2:
                            text = text[0] + text[1]
                        elif len(text) == 1:
                            text = text[0] + [""]
                    else:
                        text = ["lol", "BOTTOM TEXT"]  # todo random text

                    if text[0] == "." and text[1] != "":
                        text = [""] + [text[1]]
                    for att in event.obj["attachments"]:
                        if att['type'] == 'photo':
                            for img in att['photo']['sizes']:
                                if img['type'] == 'r':
                                    if DEBUG:
                                        print(img)
                                    if DEBUG:
                                        print(text)
                                    make_photo(img['url'], uuid, text)
                    if DEBUG:
                        print("от", uuid, "пришло", msg)
                elif event.type == VkBotEventType.MESSAGE_NEW and event.obj["text"] and not event.obj["attachments"]:
                    if msg not in ["шрифты", "fonts", "шрифтеки"] and msg != "ping":
                        message(uuid, """Шо вы хотите то, я не понял.\nОтправьте изображение с текстом в две строки для создания 
                    мема.\nПринимаются только картинки, не документы. Пересланные сообщения тоже не принимаются.\nЧтобы 
                    писать только в нижней строке, в первой поставьте точку.""")
                    elif msg == "ping":
                        message(uuid, choice(["ЕЩЩЁ ЖЫВ", "pong", "pong!", str(randint(120, 8000))+"ms"]))
                    elif msg not in ["шрифты", "fonts", "шрифтеки"]:
                        message(uuid, "Молодец. Этой функции ещё нет, а ты её уже нашёл. Просто молодец.")
        except requests.exceptions.ReadTimeout:
            if DEBUG:
                print("Timed out!")
