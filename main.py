# coding=utf8
from tokenize import Token
from telegram.ext import Application, CommandHandler, ContextTypes

import sys
import logging

from ModeCode.CodeforcesPeekingTom.GetCodeforcesStatus import (
    CodeforcesPeekingTomAddUser, CodeforcesPeekingTomStart, CodeforcesPeekingTomStartChannelById, CodeforcesPeekingTomStartChannelByName, PeekingYou)
from ModeCode.Deadline import *
from ModeCode.CodeforcesPeekingTom import *
from telegram.ext import CommandHandler

proxy = '127.0.0.1:7890'
proxies = {
    'http': 'http://' + proxy,
    'https': 'http://' + proxy,
}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# check if the bot is working


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

# a stop command


def stop(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             parse_mode=constants.ParseMode.MARKDOWN_V2, text="Have a nice day! Goodbye!")
    sys.exit(0)

TOKEN = sys.argv[1]
print(TOKEN)
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler(["start", "help"], start))
application.add_handler(CommandHandler(
    'CFPeekingTomStart', CodeforcesPeekingTomStart))
application.add_handler(CommandHandler(
    'CFPeekingTomStartChannel', CodeforcesPeekingTomStartChannelByName))
application.add_handler(CommandHandler(
    'CFPeekingTomAddUser', CodeforcesPeekingTomAddUser))
application.add_handler(CommandHandler('stop', stop))
application.add_handler(CommandHandler('ddl', ddl))
application.run_polling()
