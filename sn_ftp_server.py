import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging

# ==========================================
# ⚙️ PRO CONFIGURATION & LOGGING
# ==========================================
# Set up professional console logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BOT_TOKEN = '842571100356:AAHex14zhojqhuTs1rYx-coT8YiXPfHOYSSqk'
ADMIN_GROUP_ID = -5261477140_best 
SERVER_LINK = 'http://100.100.100.6/'
TV_SERVER_LINK = 'http://100.100.100.2'
ICC_FTP_LINK = 'http://10.16.100.244/'

bot = telebot.TeleBot(BOT_TOKEN, parse_mode='Markdown')

# ==========================================
# 🚀 /start & /help COMMAND (Menu & Links)
# ==========================================
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🌐 Movies Server", url=SERVER_LINK))
    markup.add(InlineKeyboardButton("📺 TV Server", url=TV_SERVER_LINK))
    markup.add(InlineKeyboardButton("⚡ ICC FTP Server", url=ICC_FTP_LINK))

    welcome_text = (
        "👋 **Welcome to the SN EMBY & ICC FTP Bot!**\n\n"
        "I am here to help you access the servers and request new content.\n\n"
        "🛠️ **Command Menu:**\n"
        "• `/request_movie [Name]` - Request a Movie\n"
        "• `/request_tv [Name]` - Request a TV Show\n"
        "• `/request_game [Name]` - Request a PC/Console Game\n"
        "• `/request_others [Name]` - Request Software/Music/Misc\n"
        "• `/help` - Show this menu again\n\n"
        "👇 **Click the buttons below to access the servers:**"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)
    logging.info(f"User {message.from_user.id} started the bot.")

# ==========================================
# 🛠️ CORE REQUEST ENGINE (Helper Function)
# ==========================================
def process_request(message, req_type, command_string):
    """Handles extracting text, formatting, and sending to admin with buttons."""
    request_text = message.text.replace(command_string, '').strip()
    
    if not request_text:
        bot.reply_to(message, f"⚠️ Please include the name!\n\n*Format:* `{command_string} Name`")
        return

    user = message.from_user
    username = f"(@{user.username})" if user.username else ""
    user_id = user.id

    admin_msg = (
        f"🚨 **NEW {req_type.upper()} REQUEST** 🚨\n\n"
        f"👤 **From:** {user.first_name} {username}\n"
        f"🆔 **User ID:** `{user_id}`\n"
        f"📦 **Item:** `{request_text}`" 
    )

    # 🎛️ Create Admin Action Buttons
    markup = InlineKeyboardMarkup()
    # Callback data carries the action and the user_id back to the bot
    btn_approve = InlineKeyboardButton("✅ Approve", callback_data=f"admin_act|approve|{user_id}")
    btn_deny = InlineKeyboardButton("❌ Deny", callback_data=f"admin_act|deny|{user_id}")
    markup.row(btn_approve, btn_deny)

    try:
        bot.send_message(ADMIN_GROUP_ID, admin_msg, reply_markup=markup)
        bot.reply_to(message, f"✅ Request for **{request_text}** sent to admin!")
        logging.info(f"New {req_type} request from {user_id}: {request_text}")
    except Exception as e:
        logging.error(f"Failed to send to admin group: {e}")
        bot.reply_to(message, "❌ System Error: Could not reach the admin group.")

# ==========================================
# 📥 USER REQUEST HANDLERS
# ==========================================
@bot.message_handler(commands=['request_movie'])
def handle_movie(message):
    process_request(message, "Movie", "/request_movie")

@bot.message_handler(commands=['request_tv'])
def handle_tv(message):
    process_request(message, "TV Show", "/request_tv")

@bot.message_handler(commands=['request_game'])
def handle_game(message):
    process_request(message, "Game", "/request_game")

@bot.message_handler(commands=['request_others'])
def handle_others(message):
    process_request(message, "Misc Item", "/request_others")

# ==========================================
# 🎛️ ADMIN BUTTON CLICK HANDLER
# ==========================================
@bot.callback_query_handler(func=lambda call: call.data.startswith("admin_act|"))
def handle_admin_decision(call):
    # Unpack the hidden data in the button
    _, action, target_user_id = call.data.split("|")
    
    original_msg_text = call.message.text
    
    try:
        if action == "approve":
            # 1. Update Admin Group Message (Removes buttons so it can't be clicked twice)
            bot.edit_message_text(f"{original_msg_text}\n\n✅ **STATUS: APPROVED by Admin**", 
                                  chat_id=call.message.chat.id, 
                                  message_id=call.message.message_id)
            # 2. Notify the User directly
            bot.send_message(target_user_id, "🎉 **Good news!** Your recent request has been **Approved** and will be added soon!")
            bot.answer_callback_query(call.id, "Approved & User Notified!")
            
        elif action == "deny":
            # 1. Update Admin Group Message
            bot.edit_message_text(f"{original_msg_text}\n\n❌ **STATUS: DENIED by Admin**", 
                                  chat_id=call.message.chat.id, 
                                  message_id=call.message.message_id)
            # 2. Notify the User directly
            bot.send_message(target_user_id, "😔 **Update:** Your recent request was **Denied** (it may already exist or we cannot find it).")
            bot.answer_callback_query(call.id, "Denied & User Notified!")
            
    except Exception as e:
        logging.error(f"Error handling admin callback: {e}")
        bot.answer_callback_query(call.id, "⚠️ Error notifying user. They may have blocked the bot.", show_alert=True)

# ==========================================
# 🤖 AUTO-REPLY
# ==========================================
@bot.message_handler(func=lambda message: True)
def auto_reply(message):
    bot.reply_to(message, "🤖 I only understand commands.\nType `/help` or `/start` to see the menu.")

# ==========================================
# 🏃‍♂️ RUN THE BOT
# ==========================================
logging.info("🚀 PRO Bot is successfully running and polling...")
bot.infinity_polling()