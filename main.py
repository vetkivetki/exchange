import telebot


from config import *
from extentions import *
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = "Привет! Я помогаю перевести деньги из одной валюты в другую. Формат ввода: трехбуквенное обозначение начальной валютты, валюта перевода, сумма."
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['help'])
def start(message: telebot.types.Message):
    text = "Привет! Чтобы узнать доступные валюты: /values. Пример ввода: RUB, USD, 100."
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        command = message.text.split()
        if len(command) != 3:
            raise ValueError("Неправильный ввод")
        base_key, sum_key, amount = command
        new_price = Converter.get_price(base_key, sum_key, amount)
        bot.reply_to(message, f"Цена {amount} {base_key.upper()} в {sum_key.upper()} : {new_price}")
    except ValueError as e:
        bot.reply_to(message, f"Неправильный ввод\nНе хватает одного или нескольких параметров")
    except ApiException as e:
        bot.reply_to(message, f"Ошибка:\n{e}")

bot.polling()
