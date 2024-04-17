import telebot
from telebot import types
import json

token = '6986140628:AAHd0p_zk6BPvhwHHUW9z3UuAVgIq4Cv5Sc'
bot = telebot.TeleBot(token)

active_theme = None
active_question = None
active_answer = None


def add_next_question(message):
    global active_answer, active_question
    file = open('theme.json', 'r', encoding='utf-8')
    themes = json.load(file)
    file.close()
    file = open('theme.json', 'w+', encoding='utf-8')
    themes[active_theme]['questions'][active_question][active_answer] = message.text
    themes[active_theme]['questions'][message.text] = {}
    json.dump(themes, file, ensure_ascii=False)
    file.close()
    bot.send_message(message.from_user.id, text='Отправьте сообщение для вопроса')
    active_question = message.text
    bot.register_next_step_handler(message, add_answer)

def add_answer(message):
    global active_question, active_answer
    file = open('theme.json', 'r', encoding='utf-8')
    themes = json.load(file)
    file.close()
    active_answer = message.text
    file = open('theme.json', 'w+', encoding='utf-8')
    themes[active_theme]['questions'][active_question][message.text] = ''
    json.dump(themes, file, ensure_ascii=False)
    file.close()
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='Вопрос', callback_data='Добавить следующий вопрос')
    button2 = types.InlineKeyboardButton(text='Ответ', callback_data='Добавить ответ')
    keyboard.add(button1, button2)
    bot.send_message(message.from_user.id, text='Что хотите добавить?', reply_markup=keyboard)
def add_theme(message):
    global active_theme
    file = open('theme.json', 'r', encoding='utf-8')
    themes = json.load(file)
    file.close()
    file = open('theme.json', 'w+', encoding='utf-8')
    themes[message.text] = {
        "questions": {}
    }
    json.dump(themes, file, ensure_ascii=False)
    file.close()
    active_theme = message.text
    file.close()
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='Да', callback_data='Добавить вопрос')
    button2 = types.InlineKeyboardButton(text='Нет', callback_data='Не добавлять вопрос')
    keyboard.add(button1, button2)
    bot.send_message(message.from_user.id, text='Хотите добавить вопросы для данной темы?', reply_markup=keyboard)

def add_question(message):
    global active_question
    file = open('theme.json', 'r', encoding='utf-8')
    themes = json.load(file)
    file.close()
    file = open('theme.json', 'w+', encoding='utf-8')
    themes[active_theme]['questions'][message.text] = {}
    json.dump(themes, file, ensure_ascii=False)
    file.close()
    active_question = message.text
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='Да', callback_data='Добавить ответ')
    button2 = types.InlineKeyboardButton(text='Нет', callback_data='Не добавлять ответ')
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, text='Хотите добавить ответ на вопрос?', reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def get_message(message):
    print(message)
    if message.text == '/start':
        file = open('admins.json', 'r', encoding='utf-8')
        admins = json.load(file)
        file.close()
        if str(message.from_user.id) in admins.keys():
            bot.send_message(message.from_user.id, text='У Вас есть доступ к Телеграм боту')
        else:
            bot.send_message(message.from_user.id, text='вали отсюд какашк')
            exit()
        # Создание меню с командами бота
        bot.set_my_commands(
            # Указываем список команд
            commands=[
                types.BotCommand('/start', 'Начать работу с ботом'),
                types.BotCommand('/add_subject', 'Добавить новую тему')
            ],
            scope=types.BotCommandScopeChat(message.chat.id))
    if message.text == '/add_subject':
        bot.send_message(message.from_user.id, text='Введите название темы для общения')
        bot.register_next_step_handler(message, add_theme)

# Добавить обработчик нажатия на кнопки из бота
@bot.callback_query_handler(func=lambda call: True)
# Функция обработки нажатия на кнопку
def callback_worker(call):
    if call.data == 'Добавить вопрос':
        bot.send_message(call.message.chat.id, text='Напишите текст вопроса')
        bot.register_next_step_handler(call.message, add_question)
    if call.data == 'Не добавлять ответ':
        bot.send_message(call.message.chat.id, text='Для вопросов будут использованы ответы "Да/Нет"')
        bot.register_next_step_handler(call.message, add_question)
    if call.data == 'Добавить ответ':
        bot.send_message(call.message.chat.id, text='Введите ответ к вопросу')
        bot.register_next_step_handler(call.message, add_answer)
    if call.data == 'Добавить следующий вопрос':
        bot.send_message(call.message.chat.id, text='Введите следующий вопрос')
        bot.register_next_step_handler(call.message, add_next_question)




bot.polling(none_stop=True)

