import telebot
import google.generativeai as genai
import datetime

# 1. TOKENLARNI QO'YING
BOT_TOKEN = '8529832810:AAE_naPz4_FlQfyYLnAK0FB8LvzLMB9cd3s' # @BotFather'dan olingan
GEMINI_KEY = 'AIzaSyA27a0zXnhC7f6wCm0Mk0eU3RW0vJtyNL4' # Google AI Studio'dan olingan

# 2. SOZLAMALAR
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-3-flash-preview')
bot = telebot.TeleBot(BOT_TOKEN)

user_sessions = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Salom! Men Gemini AI botiman. Savol bering.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    if user_id not in user_sessions:
        user_sessions[user_id] = model.start_chat(history=[])
    
    hozir = datetime.datetime.now().strftime("%Y-%m-%d, %A")
    prompt = f"[Tizim: Bugun {hozir}]. Foydalanuvchi: {message.text}"

    try:
        bot.send_chat_action(user_id, 'typing')
        response = user_sessions[user_id].send_message(prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Xatolik yuz berdi. API kalitni tekshiring.")

print("Bot ishga tushdi...")
bot.infinity_polling()
