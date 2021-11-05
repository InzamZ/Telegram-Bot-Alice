import json
from json import encoder
import random
import datetime
from telegram import ParseMode

timezone = datetime.timezone(datetime.timedelta(hours=8))
now = datetime.datetime.now(timezone)


def ddl_cmp(a):
    return datetime.datetime.fromisoformat(a['deadline'])


def load_json(DDLFilePath="./Data/ddl.json"):
    ddl_list = []
    with open(DDLFilePath, "r", newline="", encoding="GBK") as f:
        ddl_dict = json.load(f)
        for x in ddl_dict:
            ddl_list.append(x)
    ddl_list = sorted(ddl_list, key=ddl_cmp)
    return ddl_list


def save_json(DDLFilePath="./Data/ddl.json", src=None):
    with open(DDLFilePath, "w", encoding="GBK") as f:
        f.write(json.dumps(src, indent=4, ensure_ascii=False))


def get_ddl_msg(ddl_list):
    cnt = 0
    msg_str = "Here are the *TODO* list:\n"
    msg_str += ("Now is *" + now.ctime() + "*\n")
    for x in ddl_list:
        item_datetime = datetime.datetime.fromisoformat(x['deadline'])
        if item_datetime < now:
            msg_str += ('_' + "\# " + str(cnt) + " " + item_datetime.ctime() +
                        " " + x['todo'] + "_\n")
        elif item_datetime > now + datetime.timedelta(days=7):
            msg_str += ("\# " + str(cnt) + " " +
                        item_datetime.ctime() + " " + x['todo'] + "\n")
        else:
            msg_str += ("*" + "\# " + str(cnt) + " " + item_datetime.ctime() +
                        " " + x['todo'] + "*\n")
        cnt = cnt + 1
    return msg_str


def ddl(update, context):
    ddl_list = load_json()
    if (len(context.args) == 0):
        # print(get_ddl_msg(ddl_list))
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 parse_mode=ParseMode.MARKDOWN_V2, text=get_ddl_msg(ddl_list))
    elif context.args[0] == "add":
        # print("add")
        if (len(context.args) != 3):
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Wrong number args!")
#            msg_str += "{id} \n"
#            msg_str += "Example: **\n"
#            context.bot.send_message(chat_id=update.effective_chat.id,
#                                     parse_mode=ParseMode.MARKDOWN_V2, text=msg_str)
        else:
            Exc = False
            try:
                update_datetime = datetime.datetime.fromisoformat(
                    context.args[1])
            except Exception:
                Exc = True
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text=("Invalid isoformat string!" + context.args[1]))
            finally:
                pass
            if (Exc == False and (context.args[2] != "")):
                if update_datetime.tzinfo == None:
                    update_datetime = datetime.datetime.fromisoformat(
                        update_datetime.isoformat()+"+08:00")
                temp = {'deadline': update_datetime.isoformat(),
                        'todo': context.args[2]}
                ddl_list.append(temp)
                # print(ddl_list)
                save_json(src=ddl_list)
            elif Exc == False:
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text="Invilid args(3nd)! " + "'" + context.args[2] + "'")

    elif context.args[0] == "update":
        if (len(context.args) != 4):
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Wrong number args!")
#            msg_str += "{id} \n"
#            msg_str += "Example: **\n"
#            context.bot.send_message(chat_id=update.effective_chat.id,
#                                     parse_mode=ParseMode.MARKDOWN_V2, text=msg_str)
        elif (context.args[1].isdigit()):
            update_id = int(context.args[1])
            if (update_id >= len(ddl_list)):
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text="Invilid args!")
            else:
                Exc = False
                try:
                    update_datetime = datetime.datetime.fromisoformat(
                        context.args[3])
                except Exception:
                    Exc = True
                    context.bot.send_message(
                        chat_id=update.effective_chat.id, text=("Invalid isoformat string!" + context.args[3]))
                finally:
                    pass
                if (Exc == False and (context.args[2] == "deadline" or context.args[2] == "todo")):
                    items = ["deadline", "todo"]
                    print(type(ddl_list[0]))
                    if update_datetime.tzinfo == None:
                        update_datetime = datetime.datetime.fromisoformat(
                            update_datetime.isoformat()+"+08:00")
                    temp = ddl_list[update_id]
                    temp[context.args[2]] = update_datetime.isoformat()
                    print(ddl_list)
                    save_json(src=ddl_list)
                else:
                    context.bot.send_message(
                        chat_id=update.effective_chat.id, text="Invilid args (3rd)! " + "'" + context.args[2] + "'")
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Invilid args (2nd)! " + "'" + context.args[1] + "'")
#        context.bot.send_message(chat_id=update.effective_chat.id,
#                                 parse_mode=ParseMode.MARKDOWN_V2, text=get_ddl_msg(ddl_list))
    elif context.args[0] == "finish":
        # print("finish")
        if (len(context.args) != 2):
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Wrong number args!")
        elif (context.args[1].isdigit()):
            finish_id = int(context.args[1])
            if (finish_id >= len(ddl_list)):
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text="Invilid args!")
            else:
                ddl_list.pop(finish_id)
                # print(ddl_list)
                save_json(src=ddl_list)
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Invilid command! " + "'" + context.args[0] + "'")


if __name__ == "__main__":
    msg_str = "Here are the *TODO* list:\n"
    ddl_list = load_json()
    for x in ddl_list:
        item_datetime = datetime.datetime.fromisoformat(x['deadline'])
        if item_datetime < now:
            msg_str += ('~' + item_datetime.ctime() + " " + x['todo'] + "~\n")
        elif item_datetime > now + datetime.timedelta(days=7):
            msg_str += (item_datetime.ctime() + " " + x['todo'] + "\n")
        else:
            msg_str += ("*" + item_datetime.ctime() + " " + x['todo'] + "*\n")
    print(msg_str)
