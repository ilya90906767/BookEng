import telebot 
import os
from dotenv import load_dotenv
from telebot import types
from main.book import Book
from main.database import *

create_table()
Martin_Eden = Book('main/books/Martin_Eden.txt')

load_dotenv()
MY_TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(MY_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    get_users() 
    bot.send_message(message.chat.id, "Hello, I'm a BookEng AI and i want to teach you some english...")
    if is_user_exist(message.chat.id) == True:
        bot.send_message(message.chat.id, "What are you goin to read today?")
    if is_user_exist(message.chat.id) == False:
        try: 
            create_user(message.chat.id)
            bot.send_message(message.chat.id, "New at this platform? Need some help? Type /help :)")
        except Exception as error:
            bot.send_message(message.chat.id, "oops... some error ocured...")
            

@bot.message_handler(commands=['help'])
def send_welcome(message): 
    bot.reply_to(message, "There will be help message")

@bot.message_handler(commands=['read'])
def start_reading(message):
    bot.send_message(message.chat.id,Martin_Eden.getbookframe(0,10))

@bot.message_handler(commands=['test'])
def send_test(message): 
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itemPrev = types.KeyboardButton('<')
    itemNext = types.KeyboardButton('>')
    markup.add(itemPrev,itemNext)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    stop = types.KeyboardButton(text='отмена ❌')
    keyboard.add(stop)
    bot.send_message(message.chat.id, Martin_Eden.getbookframe(0,15), reply_markup=keyboard)

bot.infinity_polling()
