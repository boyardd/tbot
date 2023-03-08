import telebot
from telebot import types
TOKEN = '6233521058:AAGmt0uVEzR1_wqK2312t9DiRv6lNxls8tg'
bot = telebot.TeleBot(TOKEN)

# Создаем список доступных услуг и мастеров
services = {
    'Стрижка': {
        'Мастер 1': 1000,
        'Мастер 2': 1500,
        'Мастер 3': 2000
    },
    'Покраска': {
        'Мастер 1': 3000,
        'Мастер 2': 3500,
        'Мастер 3': 4000
    },
    'Маникюр': {
        'Мастер 1': 500,
        'Мастер 2': 800,
        'Мастер 3': 1200
    }
}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtns = [types.KeyboardButton(s) for s in services.keys()]
    markup.add(*itembtns)
    msg = bot.send_message(message.chat.id, "Выберите услугу:", reply_markup=markup)
    bot.register_next_step_handler(msg, select_service)

# Обработчик выбора услуги
def select_service(message):
    service = message.text
    if service not in services.keys():
        msg = bot.send_message(message.chat.id, "Пожалуйста, выберите услугу из предложенных в меню.")
        bot.register_next_step_handler(msg, select_service)
    else:
        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtns = [types.KeyboardButton(master) for master in services[service].keys()]
        markup.add(*itembtns)
        msg = bot.send_message(message.chat.id, "Выберите мастера для {}:".format(service), reply_markup=markup)
        bot.register_next_step_handler(msg, select_master, service)

# Обработчик выбора мастера
def select_master(message, service):
    master = message.text
    if master not in services[service].keys():
        msg = bot.send_message(message.chat.id, "Пожалуйста, выберите мастера из предложенных в меню.")
        bot.register_next_step_handler(msg, select_master, service)
    else:
        price = services[service][master]
        bot.send_message(message.chat.id, "Вы выбрали {} у мастера {}. Стоимость: {} руб.".format(service, master, price))

bot.polling()
