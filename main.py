from vk_api import vk_api
from config import *
import datetime
import time
import smtplib
import os
import time
import mimetypes
from pyfiglet import Figlet
from tqdm import tqdm
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

new_id = '1'
new_text = '2'
old_id = '3'
old_text = '4'
count_s = 0

vk_session = vk_api.VkApi(app_id=2274003, token=token, scope='messages')
vk = vk_session.get_api()


while True:
    time.sleep(0.5)
    now = datetime.datetime.now()

    month = '%d' % now.month
    day = '%d' % now.day
    hour = '%d' % now.hour
    minute = '%d' % now.minute
    second = '%d' % now.second
    date = str(day) + '.' + str(month) + '|' + str(hour) + \
        ':' + str(minute) + ':' + str(second)

    #massages = vk.messages.getConversations(filter="unread")
    massages = vk.messages.getDialogs(unread=0)

    try:
        user_id = int(massages['items'][0]['message']['user_id'])
        if user_id < 0:
            s = 0
        else:
            user_id = str(user_id)
            s = 1
    except:
        pass

    try:
        if s == 0:
            pass
        else:
            user_id = massages['items'][0]['message']['user_id']
        text = massages['items'][0]['message']['body']
        new_text = text
        new_id = user_id

    except:
        continue

    if new_id and new_text == old_text and old_id:
        continue
    else:
        pass

    if s == 0:
        fullname = 'Сообщество'
    else:
        user = vk_session.method("users.get", {"user_ids": user_id})
        fullname = user[0]['first_name'] + ' ' + user[0]['last_name']

    try:
        url = massages['items'][0]['message']['attachments']

        a = url.photo.sizes
        print(massages['items'][0]['message']['attachments'].photo.sizes)
        z = []
        for i in a:
            z.append({"url": i.url, "width": i.width})
        z.sort(key=operator.itemgetter("width"))
        print(z[len(z) - 1]["url"])

        photo_bytes = request(z[len(z) - 1]["url"])
        print(z[len(z) - 1]["url"])
    except:
        pass

    if text == '':
        print('Пользователь: ' + str(fullname) + ' [ID:' + str(
            user_id) + '] | ' + 'Время: ' + '[' + str(date) + '] | ' + 'Текст: *URL* \n')
        a = 'Пользователь: ' + str(fullname) + ' [ID:' + str(
            user_id) + '] | ' + 'Время: ' + '[' + str(date) + '] | ' + 'URL: ' + str(url) + '\n'
        file = open('vk.txt', 'a', encoding="utf-8")
        file.write(a)
        file.close()
        old_text = text
        old_id = new_id
        count_s += 1
        print(count_s)

    else:
        b = 'Пользователь: ' + str(fullname) + ' [ID:' + str(
            user_id) + '] | ' + 'Время: ' + '[' + str(date) + '] | ' + 'Текст: ' + str(text) + '\n'
        print(b)
        file = open('vk.txt', 'a', encoding="utf-8")
        file.write(b)
        file.close()
        old_text = text
        old_id = new_id
        count_s += 1
        print(count_s)
    if count_s == 50:
        try:
            server.login(sender, password)
            msg = MIMEMultipart()
            msg["From"] = sender
            msg["To"] = owner_bot
            msg["Subject"] = "Лог отчет 50 сообщений!"
            filename = "vk.txt"

            print("Sending...")
            with open(f"vk.txt", "rb") as f:
                file = MIMEApplication(f.read())
                file.add_header('content-disposition',
                                'attachment', filename=filename)
                msg.attach(file)

            server.sendmail(sender, sender, msg.as_string())

            print("The message was sent successfully!")
        except Exception as _ex:
            print(f"{_ex}\nCheck your login or password please!")
    else:
        pass
