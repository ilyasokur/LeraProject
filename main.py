import sqlite3
import telebot
from telebot import types

token = "5340804566:AAFQ1yUi7mcOqcK2nrdxH2D3Qc5SWthBtgc"
bot = telebot.TeleBot(token)


def get_info(db_file, date_to_get):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    info = cursor.execute("SELECT * FROM `sign` WHERE `date` = ?", (date_to_get,))
    result = ''
    for res in info:
        result = res
    return result


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, 'Здравствуйте! Мы собрали ответы на самые популярные вопросы о знаках '
                                           'зодиака. Здесь вы узнаете об особенностях своего астрологического знака и '
                                           'о том, к какому «звёздному» специалисту стоит обратиться!')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Характеристики знака')
    item2 = types.KeyboardButton('Помощь специалиста')
    markup.add(item1, item2)
    bot.send_message(message.from_user.id, "Что вас интересует?", reply_markup=markup)


@bot.message_handler()
def buttons_action(message):
    if message.text == 'Характеристики знака':
        msg = bot.send_message(message.from_user.id, 'Введите дату рождения (Число.Месяц)')
        bot.register_next_step_handler(msg, bot_message)

    elif message.text == 'Помощь специалиста':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_1 = types.KeyboardButton('Астролог')
        item_2 = types.KeyboardButton('Астропсихолог')
        item_3 = types.KeyboardButton('Таролог')
        item_4 = types.KeyboardButton('Вернуться в начало')
        markup.add(item_1, item_2, item_3, item_4)
        bot.send_message(message.from_user.id, 'Выберите специалиста, чтобы узнать, зачем к нему обращаются',
                         reply_markup=markup)

    elif message.text == 'Астролог':
        with open('astr.txt', 'r') as f:
            info = f.read()
            bot.send_message(message.from_user.id, info)

    elif message.text == 'Астропсихолог':
        with open('psy.txt', 'r') as f:
            info = f.read()
            bot.send_message(message.from_user.id, info)

    elif message.text == 'Таролог':
        with open('tar.txt', 'r') as f:
            info = f.read()
            bot.send_message(message.from_user.id, info)

    elif message.text == 'Вернуться в начало':
        start(message)

    else:
        bot.send_message(message.from_user.id, 'Данные не корректны')


def bot_message(message):
    db_file = 'sign.db'
    lst_of_dates = ['21.03-20.04', '21.04-20.05', '21.05-20.06', '21.06-22.07', '23.07-22.08',
                    '23.07-22.08', '23.09-22.10',
                    '23.10-22.11', '23.11-21.12', '22.12-19.01', '20.01-19.02', '20.02-20.03']
    try:
        check = message.text
        check = check.split('.')
        day, month = check[0], check[1]
        flag = False
        for i in lst_of_dates:
            p = i.split('-')
            start_ = p[0].split('.')
            end_ = p[1].split('.')
            if int(day) >= int(start_[0]) and int(month) == int(start_[1]) or int(day) <= int(end_[0]) and int(
                    month) == int(end_[1]):
                flag = True
                break
        info = ['Знак зодиака: ', 'Стихия: ', 'Планета-покровитель: ', 'Камень-талисман: ', 'Цвет силы: ', 'Талисман: ']

        if flag:
            result = get_info(db_file, i)[1:]
            for i in range(len(info)):
                bot.send_message(message.from_user.id, info[i] + result[i])
        else:
            bot.send_message(message.from_user.id, 'Данные не корректны')

    except:
        bot.send_message(message.from_user.id, 'Данные не корректны')


if __name__ == '__main__':
    bot.infinity_polling()
