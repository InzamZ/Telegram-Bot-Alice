import json
import random
import datetime

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
    ddl_list = sorted(ddl_list,key=ddl_cmp)
    return ddl_list

def ddl(update,context):
    msg_str_all = "Here are the TODO list:\n"
    msg_str_warning = "\033[1;31m"
    ddl_list = load_json()
    for x in ddl_list:
        item_datetime = datetime.datetime.fromisoformat(x['deadline'])
        msg_str_all += (item_datetime.ctime() + " " + x['todo'] + "\n")
        if item_datetime <= now + datetime.timedelta(days=7):
            msg_str_warning += (item_datetime.ctime() + " " + x['todo'] + "\n")
    msg_str_warning += "\033[0m"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg_str_all)


    
