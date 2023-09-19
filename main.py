import telebot
import os
from telebot import types
from instagram_api import Client 
from fastapi import FastAPI

bot = telebot.TeleBot(TELEGRAM_TOKEN)
insta_client = Client(INSTA_USER, INSTA_PASS)

app = FastAPI()

user_data = {}

@bot.message_handler(commands=['start']) 
def start(message):

  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  login_btn = types.KeyboardButton("Login to Instagram")
  help_btn = types.KeyboardButton("Help")
  settings_btn = types.KeyboardButton("Settings")
  
  markup.add(login_btn, help_btn, settings_btn)
  
  bot.send_message(message.chat.id, 
                   "Welcome! This bot can upload videos from Telegram to Instagram. Select an option below:",
                   reply_markup=markup)
  
# Other handlers like help, settings  

@bot.message_handler(func=lambda msg: msg.text == "Login to Instagram")
def insta_login(message):

  msg = bot.send_message(message.chat.id, "Please enter your Instagram username:")
  bot.register_next_step_handler(msg, insta_username)

def insta_username(message):
  user_data['insta_username'] = message.text
  
  msg = bot.send_message(message.chat.id, "Please enter your Instagram password:")
  bot.register_next_step_handler(msg, insta_password) 

def insta_password(message):
  user_data['insta_password'] = message.text
  
  try:
    insta_client.login(user_data['insta_username'], user_data['insta_password'])
    bot.send_message(message.chat.id, "Logged in successfully!")
    
    # Show Instagram stats etc
    # Create menu for uploading, scheduling, autoreply, logout
  
  except:
    bot.send_message(message.chat.id, "Invalid login credentials!")
    insta_login(message) # retry login

# Handlers for upload, scheduling, autoreply, logout

@bot.message_handler(content_types=['video'])
def upload_video(message):

  # Download and upload video to Instagram
  bot.send_message(message.chat.id, "Video uploaded!")

@app.get("/healthz")  
def healthcheck():
  return {"ok": True}

if __name__ == "__main__":

  bot.infinity_polling()
  
  app.run()
