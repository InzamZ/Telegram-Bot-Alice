from telegram.ext import CommandHandler
from ModeCode.Deadline import *
from telegram.ext import Updater, JobQueue
import sys
import logging
import datetime

with open("token.secret.me", "r") as f:
    TOKEN = f.readline()
    TOKEN = TOKEN.strip()
    f.close()

with open("id.secret.me", "r") as f:
    ME = f.readline()
    ME = ME.strip()
    f.close()

updater = Updater(token=TOKEN, use_context=True)
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

# print ddl list

# TODO:不能使用context send message，考虑如何发送给自己
print(ME)
jobqueue.run_daily(daily_notice(bot, ME), name="daily_notice", time=datetime.time(
    hour=16, minute=24, tzinfo=timezone.utc))
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

updater.start_polling(timeout=3)
