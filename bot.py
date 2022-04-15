from time import sleep
import telebot
import cv2
import requests
from pathlib import Path
import os

pwd = Path.cwd()

import detection as det

path = "F:/Users/admin/Desktop/bot/"

TOKEN = '5106687890:AAG_kraeLbAPMz1HKqoRbGR19FbnijgiNoQ' 
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Hello, send picture with Kitty :з UwU')
# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, 'just send me photo')
countOfCats = 0
# getFile
# Downloading a file is straightforward
# Returns a File object
@bot.message_handler(content_types='photo')
def take_photo(message):
    global countOfCats
    file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
    bot.send_message(message.chat.id, 'Please, wait...')
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path))
    countOfCats += 1
    nameFile = f'Picture/temp{countOfCats}.jpg'
    cv2.imwrite(path+nameFile, det.outlineCats(file.content, path+'best.pt'))
    bot.send_photo(message.chat.id, open(path+nameFile, 'rb'))
    print('sended')
    #TODO: сделать название класса, вывод вероятности, опознование на видео и на несколько отправленных фото, удаление temp файлов после Nого temp


# Запускаем бота
print('start')
bot.polling(none_stop=True, interval=0)