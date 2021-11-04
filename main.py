from telegram.ext import Updater
import logging

with open("token.secret.me","r") as f:
    TOKEN = f.read()

updater = Updater(token=TOKEN, use_context=True)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# check if the bot is working
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

#end

# print ddl list
from ModeCode.Deadline import *

def ddl(update, context):
    msg_list = getddl()
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg_list[0])

ddl_handler = CommandHandler('ddl', ddl)
dispatcher.add_handler(ddl_handler)

updater.start_polling()
