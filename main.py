from telegram import update
from telegram.ext import CommandHandler, MessageHandler
from ModeCode import LoadConf
from ModeCode.Deadline import *
from ModeCode.LoadConf import *
from telegram.ext import Updater
import sys
import logging
import datetime

updater = Updater(token=LoadConf.conf['bot']['token'], use_context=True)
bot = updater.bot
jobqueue = updater.job_queue
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# check if the bot is working


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# end

# ddl

jobqueue.run_daily(ddl_daily_notice, name="ddl_daily_notice", time=datetime.time.fromisoformat(LoadConf.conf['time']))
ddl_handler = CommandHandler('ddl', ddl)
dispatcher.add_handler(ddl_handler)

# end

# a stop command


def stop(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Have a nice day! Goodbye!")
    updater.stop()
    sys.exit(0)


stop_handler = CommandHandler('stop', stop)
dispatcher.add_handler(stop_handler)

updater.start_polling()
