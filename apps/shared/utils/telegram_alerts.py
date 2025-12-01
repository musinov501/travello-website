import threading
import telebot
import html
from core import config

bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)

def _send_telegram_message(text: str):
    try:
        bot.send_message(
            chat_id=config.TELEGRAM_CHANNEL_ID,
            text=text,
            parse_mode='HTML',
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

def send_alert(text: str):
    """Send Telegram alert in background thread."""
    threading.Thread(target=_send_telegram_message, args=(text,), daemon=True).start()
