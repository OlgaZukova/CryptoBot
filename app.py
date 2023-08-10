
import telebot
from config import keys,TOKEN
from utils import ConvertionExeption, CryptoConverter


bot = telebot.TeleBot(TOKEN)

# @bot.message_handler(commands=["site", "website"])
# def site(message):
#     webbrowser.open("https://valuta.exchange/")

# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
# @bot.message_handler(commands=['start', 'main', 'Hello', 'hello', 'Hello!','hello!'])
# def main(message):
#     bot.send_message(message.chat.id, f"Привет! {message.from_user.first_name} {message.from_user.last_name}")

@bot.message_handler(commands=['start', 'help'])
def help(message:telebot.types.Message):
    text = 'Чтобы начать введите команду боту в следующем формате:\n<имя валюты>\
<в какую валюту перевести>\
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values'

    bot.reply_to(message,text)

@bot.message_handler(commands=['values'])
def values(message:telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message,text)

@bot.message_handler(content_types=['text', ])
def convert(message:telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionExeption('Слишком много параметров')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionExeption as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message,f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(non_stop=True)