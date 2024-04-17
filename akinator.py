
questions = {
}

answers = []

current_question = ''
questions = {}
current_theme = ''


import telebot
from telebot import types
import json

token = '7134715700:AAEaJiinVBNVuV9pdbVYJGerAaKXhfEa934'
bot = telebot.TeleBot(token)

file = open('theme.json', 'r', encoding='utf-8')
themes = json.load(file)
file.close()


@bot.message_handler(content_types=['text'])
def get_message(message):
    if message.text == '/start':
        # Создание меню с командами бота
        bot.set_my_commands(
            # Указываем список команд
            commands=[
                types.BotCommand('/start', 'Начать диалог с ботом'),
                ],
            scope = types.BotCommandScopeChat(message.chat.id)
        ),
        keyboard = types.InlineKeyboardMarkup()
        for theme in list(themes.keys()):
            button = types.InlineKeyboardButton(text=theme, callback_data='theme_'+theme)
            keyboard.add(button)
        bot.send_message(message.from_user.id, text='Выберите тему для общения', reply_markup=keyboard)

# Добавить обработчик нажатия на кнопки из бота
@bot.callback_query_handler(func=lambda call: True)
# Функция обработки нажатия на кнопку
def callback_worker(call):
    global current_question, answers, questions, current_theme

    if call.data.startswith('theme'):
        current_theme = call.data.split('_')[1]
        file = open('theme.json', 'r', encoding='utf-8')
        themes = json.load(file)
        file.close()
        questions = themes[current_theme]['questions']
        current_question = list(questions.keys())[0]

        keyboard1 = types.InlineKeyboardMarkup()
        for answer in list(themes[current_theme]['questions'][current_question].keys()):
            button11 = types.InlineKeyboardButton(text=answer, callback_data='answer_'+answer)
            keyboard1.add(button11)
        bot.send_message(call.message.chat.id, text=current_question, reply_markup=keyboard1)
    elif call.data.startswith('answer'):
        file = open('theme.json', 'r', encoding='utf-8')
        themes = json.load(file)
        file.close()
        answer = call.data.split('_')[1]
        current_question = questions[current_question][answer]
        if current_question == '':
            bot.send_message(call.message.chat.id, text='Вы ответили на все вопросы')
        else:
            keyboard1 = types.InlineKeyboardMarkup()
            for answer in list(themes[current_theme]['questions'][current_question].keys()):
                button11 = types.InlineKeyboardButton(text=answer, callback_data='answer_' + answer)
                keyboard1.add(button11)
            bot.send_message(call.message.chat.id, text=current_question, reply_markup=keyboard1)




bot.polling(none_stop=True, interval=0)
