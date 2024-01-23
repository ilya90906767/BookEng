import telebot 
import os
from dotenv import load_dotenv
from telebot import types
from main.book import Book
from main.database import *

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
            add_user(message.chat.id)
            bot.send_message(message.chat.id, "New at this platform? Need some help? Type /help :)")
        except Exception as error:
            bot.send_message(message.chat.id, "oops... some error ocured...")
            


@bot.message_handler(commands=['upload'])
def upload_welcome(message):
    bot.send_message(message.chat.id, "Okay, just upload your book. Now we can process only .txt files")
    bot.register_next_step_handler(message, process_file)
    
def process_file(message):
    try: 
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = f"/home/ilyabetyaev/petprojects/BookEng/main/books/" + message.document.file_name
        
        with open(src, "wb") as new_file:
            new_file.write(downloaded_file)
        
        add_book(message.chat.id,message.document.file_name,src)
        bot.reply_to(message,"File was upload succesfully")
    except Exception as e:
        bot.reply_to(message,e)
        
    
@bot.message_handler(commands=['help'])
def send_welcome(message): 
    bot.reply_to(message, "There will be help message")



@bot.message_handler(commands=['mybooks'])
def mybooks(message):
    user_books = get_user_books(message.chat.id)
    str_of_books = ''
    for book in user_books:
        str_of_books = str_of_books + book[2] + " "
        
    bot.send_message(message.chat.id,str_of_books )


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
