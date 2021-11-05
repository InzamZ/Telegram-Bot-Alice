import json
import random
import datetime
from telegram import ParseMode

timezone = datetime.timezone(datetime.timedelta(hours=8))
now = datetime.datetime.now(timezone)


def ddl_cmp(a):
    return datetime.datetime.fromisoformat(a['deadline'])

def load_json():
    ddl_list = []
    with open("ddl.json", "r", newline="") as f:
        ddl_dict = json.load(f)
        for x in ddl_dict:
            ddl_list.append(x)
    ddl_list = sorted(ddl_list, key=ddl_cmp)
    return ddl_list


def ddl(update, context):
    msg_str= "Here are the *TODO* list:\n"
    ddl_list = load_json()
    for x in ddl_list:
        item_datetime = datetime.datetime.fromisoformat(x['deadline'])
        if item_datetime < now :
            msg_str += ('~' + item_datetime.ctime() + " " + x['todo'] + "~\n")
        elif item_datetime > now + datetime.timedelta(days=7):
            msg_str += (item_datetime.ctime() + " " + x['todo'] + "\n")
        else:
            msg_str += ("*" + item_datetime.ctime() + " " + x['todo'] + "*\n")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             parse_mode=ParseMode.MARKDOWN_V2, text=msg_str)

if __name__ == "__main__":
    msg_str= "Here are the *TODO* list:\n"
    ddl_list = load_json()
    for x in ddl_list:
        item_datetime = datetime.datetime.fromisoformat(x['deadline'])
        if item_datetime < now :
            msg_str += ('~' + item_datetime.ctime() + " " + x['todo'] + "~\n")
        elif item_datetime > now + datetime.timedelta(days=7):
            msg_str += (item_datetime.ctime() + " " + x['todo'] + "\n")
        else:
            msg_str += ("*" + item_datetime.ctime() + " " + x['todo'] + "*\n")
    print(msg_str)

    