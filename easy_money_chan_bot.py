import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter, Index

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_def(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту  следущем формате:\n"имя валюты" "в какую валюту перевести" ' \
           '"количество переводимой валюты" \nПример: "доллар рубль 2"\n' \
           '\nЧтобы увидеть список доступных валют введите команду "/values"' \
           '\nЧтобы узнать текущий курс валют в рублях введите команду "/index"'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(commands=['index'])
def index(message: telebot.types.Message):
    text = Index.get_index()
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        var = message.text.split(' ')

        if len(var) != 3:
            raise APIException('Неверное количество параметров!')

        quote, base, amount = var
        total_base = float(CryptoConverter.get_price(quote, base, amount))
        price = float(amount)*total_base
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя!\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду!\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {round(price, 2)}'
        bot.send_message(message.chat.id, text)


bot.polling()
