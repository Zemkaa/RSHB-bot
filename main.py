import telebot
from telebot import types
from RSHB import Parcing
import requests
from bs4 import BeautifulSoup
from transliterate import translit
bot = telebot.TeleBot('1214038664:AAGou_lvPbWDGLbbPqKMOfJ_Za-7xPRiL5I')
loans = Parcing.main()
buttons = []
loans.pop()
for loan in loans:
    buttons.append(loan[0])


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(True)
    for button in buttons:
        new_button = types.KeyboardButton(button)
        markup.add(new_button)
    bot.send_message(message.chat.id, 'Добрый день. Я - чат-бот для оформления заявок '
                                      'на потребительский кредит в РоссельхозБанке.'
                                      'Выберите из представленных возможностей интереующую вас.'
                                      'При выборе любого из кредитов вам будет представлена '
                                      'информация об услуге.', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def loan_info(message):
    for i in range(0, len(buttons)):
        if message.text == buttons[i]:
            if loans[i][4] != '':
                bot.send_message(message.chat.id, f"Вы выбрали кредит {buttons[i]} со ставкой от {loans[i][2]}. "
                                                  f"Данный кредит выдается на срок не более {loans[i][3]} лет. Кредит "
                                                  f"выдается на сумму до {loans[i][4]}. "
                                                  f"Более подробную информацию можно получить по ссылке: {loans[i][1]}")
                bot.register_next_step_handler(message, application_filing(message))
                break
            else:
                bot.send_message(message.chat.id, f"Вы выбрали кредит {buttons[i]} со ставкой от {loans[i][2]}. "
                                                  f"Данный кредит выдается на срок не более {loans[i][3]} лет. "
                                                  f"Более подробную информацию можно получить по ссылке: {loans[i][1]}")
                bot.register_next_step_handler(message, application_filing(message))
                break


def application_filing(message):
    markup = types.ReplyKeyboardMarkup(True)
    markup.add(f"Да, оформить кредит {message.text}", f"Нет, перейти к просмотру других возможностей")
    bot.send_message(message.chat.id, 'Хотите ли вы подать заявку на данный кредит?', reply_markup=markup)


bot.polling(none_stop=True, interval=0)
