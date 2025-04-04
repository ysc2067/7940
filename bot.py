import telebot
import openai
import configparser
from firebase_util import store_message

# 读取 config.ini
config = configparser.ConfigParser()
config.read("config.ini")

telegram_token = config["telegram"]["token"]
openai.api_key = config["openai"]["api_key"]

bot = telebot.TeleBot(telegram_token)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text

    # 使用 ChatGPT API 获取回复
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}]
    )
    reply = response.choices[0].message.content

    # 发送回复
    bot.reply_to(message, reply)

    # 储存聊天记录到 Firebase
    store_message(message.chat.id, user_input, reply)

bot.polling()
