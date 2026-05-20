import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Logging setup taaki errors terminal par saaf dikhein
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- CONFIGURATION (Tera Asli Data) ---
TELEGRAM_TOKEN = "8574538371:AAF8-qsTCU6vFPHaD6iidJCTS1Cr0rDaoAc"
DIFY_API_KEY = "app-sv5vNyebPrCSIqqGvvAWMqXx"
DIFY_API_URL = "https://api.dify.ai/v1/chat-messages"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Jab user /start dabayega tab yeh welcome message jayega."""
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"👋 Welcome {user_name} to TradeGuru!\n\n"
        "I am your world-class AI Trading Teacher. Ask me anything about Candlestick patterns, "
        "Market Structure, or Risk Management. Let's learn together! 📈🕯️"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User ke message ko Dify (Gemini) ke paas bhej kar reply laane ke liye."""
    user_text = update.message.text
    user_id = str(update.effective_user.id) # Har user ki alag chat yaad rakhne ke liye
    
    # Telegram par "typing..." status dikhane ke liye
    await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action="typing")

    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": {},
        "query": user_text,
        "response_mode": "blocking",
        "user": user_id,
        "conversation_id": ""
    }

    try:
        response = requests.post(DIFY_API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            res_data = response.json()
            bot_reply = res_data.get('answer', 'Sorry, I couldn\'t process that.')
            await update.message.reply_text(bot_reply)
        else:
            await update.message.reply_text("❌ Error: Unable to connect to TradeGuru brain. Try again later.")
    except Exception as e:
        logging.error(f"Error connecting to Dify: {e}")
        await update.message.reply_text("❌ Something went wrong. Please try again.")

def main():
    """Bot ko start karne ka main function."""
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Handlers (Commands aur Messages ko pakadne ke liye)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 TradeGuru Global Bot is running live on Telegram...")
    app.run_polling()

if __name__ == '__main__':
    main()