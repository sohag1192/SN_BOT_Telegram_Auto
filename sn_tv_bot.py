import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- CONFIGURATION ---
API_TOKEN = '8296157365:AAEKj8U9TmADMoHDjuQjJ0_alg7BH3dOVgc' 
ADMIN_ID = '8409643894' # e.g., 123456789 (See instructions below on how to get this)

bot = telebot.TeleBot(API_TOKEN)

# --- THE MESSAGE ---
UPDATE_MESSAGE = """📢 **আপডেট:**
SN TV সেবা বর্তমানে আপনার ইন্টারনেট সংযোগে উপলব্ধ নয়।
সেবা চালু করতে অনুগ্রহ করে আপনার ইন্টারনেট সেবা প্রদানকারীর সাথে যোগাযোগ করুন।
আপনাদের অসুবিধার জন্য আমরা আন্তরিকভাবে দুঃখিত।

📢 **Update:**
SN TV service is currently not available on your internet connection.
To enable access, please contact your internet service provider.
We sincerely apologize for the inconvenience."""

# --- THE UI (INLINE KEYBOARD) ---
def create_ui():
    markup = InlineKeyboardMarkup()
    # Adding a sleek button that users can click. 
    # You can change this URL to your Sarker Net support group or your direct Telegram link.
    support_button = InlineKeyboardButton("💬 Contact Support", url="https://t.me/+uVv0o1ddKyVmYWFl")
    markup.add(support_button)
    return markup

# --- ADMIN NOTIFICATION SYSTEM ---
def notify_admin(message):
    try:
        # Grabs the user's name or username
        user_name = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
        user_id = message.from_user.id
        
        # Formats the alert sent to you
        alert_text = (
            f"🚨 *New Message Alert*\n"
            f"👤 *From:* {user_name} (ID: `{user_id}`)\n"
            f"💬 *Message:* {message.text}"
        )
        
        # Sends the alert to your ADMIN_ID
        bot.send_message(ADMIN_ID, alert_text, parse_mode='Markdown')
    except Exception as e:
        print(f"Failed to notify admin: {e}")

# --- BOT HANDLERS ---
@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    # Replies to the user with the message and the sleek UI buttons
    bot.reply_to(message, UPDATE_MESSAGE, parse_mode='Markdown', reply_markup=create_ui())
    # Notifies you (the admin)
    notify_admin(message)

@bot.message_handler(func=lambda message: True)
def handle_all_other_messages(message):
    # Replies to the user
    bot.reply_to(message, UPDATE_MESSAGE, parse_mode='Markdown', reply_markup=create_ui())
    # Notifies you (the admin)
    notify_admin(message)

# Starts the bot
print("🤖 SN TV Auto-reply Bot with Admin Notifications is running...")
bot.infinity_polling()