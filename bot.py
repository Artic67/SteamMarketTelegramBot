import time
import json

import telebot
from telebot import types
import requests

file = open('credentials.json')
creds = json.load(file)
file.close()

LAUNCH_OFFSET = 0
bot = telebot.TeleBot(creds['token'])


def isCommand(message, command=None):
    if message.entities is None:
        return False

    for entity in message.entities:
        if entity.type == 'bot_command':
            if command is not None:
                if message.text.startswith('/{command}'.format(command=command)):
                    return True
                return False
            return True

def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('🐼 Профиль')
    btn2 = types.KeyboardButton('💵 Маркет')
    btn3 = types.KeyboardButton('⚙️ Настройки')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.from_user.id, 'Приветствую! Я Steam Market Helper.', reply_markup=markup)
    bot.send_message(message.from_user.id, '❓ Выберите пункт меню', reply_markup=markup)

def help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.from_user.id, 'Доступые комманды:\n\n/help - Помощь\n/info - Информация про бота\n/menu - Меню\n/profile - Профиль Steam\n/market - Меню Steam Market\n/settings - Настройки', reply_markup=markup)

def info(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.from_user.id, 'Данный бот помогает работать с Торговой площадкой в Steam и автоматизирует процесс продажи товаров, выставления ордеров как на покупку так и на продажу, также есть возможность автоизменения цены ордеров.', reply_markup=markup)

def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
    btn1 = types.KeyboardButton('🐼 Профиль')
    btn2 = types.KeyboardButton('💵 Маркет')
    btn3 = types.KeyboardButton('⚙️ Настройки')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.from_user.id, '👀 Выберите интересующий раздел', reply_markup=markup)  # ответ бота

def profile(message):
    sp = getSteamProfileToStr(message)
    bot.send_message(message.from_user.id, 'Ваш профиль Steam:\n{profile}'.format(profile=sp))  # ответ бота
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
    btn1 = types.KeyboardButton('🐼 Профиль')
    btn2 = types.KeyboardButton('💵 Маркет')
    btn3 = types.KeyboardButton('⚙️ Настройки')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.from_user.id, '👀 Выберите интересующий раздел', reply_markup=markup)  # ответ бота

def market(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
    btn1 = types.KeyboardButton('🧔 Купить')
    btn2 = types.KeyboardButton('✏️Продать')
    btn3 = types.KeyboardButton('✏️Ордер покупки')
    btn4 = types.KeyboardButton('✏️Ордер продажи')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.from_user.id, '⬇ Выберите подраздел', reply_markup=markup)  # ответ бота

def settings(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
    btn1 = types.KeyboardButton('🧔 Аккаунт')
    btn2 = types.KeyboardButton('✏️Изменить данные')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, '⬇ Выберите подраздел', reply_markup=markup)  # ответ бота

def isText(message):
    if message.content_type == "text":
        return True
    return False

def getSteamProfileToStr(message):
    return "Профиль Steam не указан"

def getAccDataToStr(message):
    return "Данные аккаунта не указаны"

def get_text_messages(message, ts, eq):

    if message.text == '📝 Меню':
        menu(message)

    elif message.text == '🐼 Профиль':
        profile(message)

    elif message.text == '💵 Маркет':
        market(message)

    elif message.text == '⚙️ Настройки':
        settings(message)

    elif message.text == '🧔 Купить':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
        eq.addEvent({
            'id': '1251234',
            'event': 'getPrice'
        })
        bot.send_message(message.from_user.id, 'Создание ордера на покупку', reply_markup=markup)  # ответ бота

    elif message.text == '✏️Ордер покупки':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
        ts.addTask({
            'id': '1251234',
            'event': 'getPrice'
        })
        bot.send_message(message.from_user.id, 'Создание создание автоордера', reply_markup=markup)  # ответ бота

    elif message.text == '✏️Ордер продажи':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
        ts.delTask('1251234')
        bot.send_message(message.from_user.id, 'Удаление автоордера', reply_markup=markup)  # ответ бота

    elif message.text == '🧔 Аккаунт':
        accdata = getAccDataToStr(message)
        bot.send_message(message.from_user.id, 'Данные вашего аккаунта:\n{acc}'.format(acc=accdata))  # ответ бота
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
        btn1 = types.KeyboardButton('🧔 Аккаунт')
        btn2 = types.KeyboardButton('✏️Изменить данные')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, '⬇ Выберите подраздел', reply_markup=markup)  # ответ бота

    elif message.text == '✏️Изменить данные':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
        btn1 = types.KeyboardButton('🧔 1')
        btn2 = types.KeyboardButton('✏️2')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, '⬇ Выберите пункт для изменения', reply_markup=markup)  # ответ бота



class EventQueue:
    def __init__(self, queue):
        self.queue = queue

    def getEvent(self):
        return self.queue.pop()

    def addEvent(self, event):
        self.queue.insert(0, event)

    def getQueue(self):
        return self.queue

    def getLength(self):
        return len(self.queue)

    def isEmpty(self):
        if len(self.queue) == 0:
            return True
        return False

class TaskStorage:
    def __init__(self, storage):
        self.storage = storage

    def saveStorage(self, filename):
        with open('storage.json', 'w') as f:
            json.dump(self.storage, f)

    def getTasks(self):
        arr = []
        for task in self.storage:
            arr.append(self.storage[task])
        return arr

    def addTask(self, task):
        self.storage[task['id']] = task
        self.saveStorage('storage.json')

    def delTask(self, id):
        self.storage.pop(id)
        self.saveStorage('storage.json')

    def isEmpty(self):
        if len(self.storage) == 0:
            return True
        return False

class EventLoop:
    def __init__(self, globalOffset):
        self.globalOffset = globalOffset

    def loadData(self, filename):
        file = open(filename)
        data = json.load(file)
        file.close()
        return data

    def launch(self):

        storage = self.loadData("storage.json")
        eq = EventQueue([])
        ts = TaskStorage(storage)


        while True:
            try:
                print(1)
                if not ts.isEmpty():
                    tasks = ts.getTasks()
                    for task in tasks:
                        print(task)

                if not eq.isEmpty():
                    for i in range(eq.getLength()):
                        event = eq.getEvent()
                        print(event)

                # bot.send_message(message.from_user.id)

                # response = requests.post(MethodGetUpdates)
                # result = response.json()
                # print(result)
                # print(offset)
                updates = bot.get_updates(offset=self.globalOffset)
                for update in updates:
                    print(update)
                    if isCommand(update.message):
                        if isCommand(update.message, "start"):
                            start(update.message)
                        elif isCommand(update.message, "help"):
                            help(update.message)
                        elif isCommand(update.message, "info"):
                            info(update.message)
                        elif isCommand(update.message, "menu"):
                            menu(update.message)
                        elif isCommand(update.message, "profile"):
                            profile(update.message)
                        elif isCommand(update.message, "market"):
                            market(update.message)
                        elif isCommand(update.message, "settings"):
                            settings(update.message)


                    elif isText(update.message):
                        get_text_messages(update.message, ts, eq)
                    self.globalOffset = update.update_id + 1
                time.sleep(1)
            except Exception as e:
                print("Error: ", e)


El = EventLoop(LAUNCH_OFFSET)
El.launch()

#bot.polling(none_stop=True, interval=0, timeout=20)
#bot.infinity_polling(interval=0, timeout=20)