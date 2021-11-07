import json
from json import encoder
import random
import datetime
from telegram import ParseMode, parsemode

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
                chat_id=update.effective_chat.id, text="ERROR: 3 args expected but " + str(len(context.args)) + " received")
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
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text="Added " + temp['deadline'] + " " + temp['todo'] + " !\n")
                save_json(src=ddl_list)
            else:
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text=("ERROR: Invalid isoformat string. " + context.args[1]) + " !\n")

    elif context.args[0] == "update":
        if (len(context.args) != 4):
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="ERROR: 4 args expected but " + str(len(context.args)) + " received.")
#            msg_str += "{id} \n"
#            msg_str += "Example: **\n"
#            context.bot.send_message(chat_id=update.effective_chat.id,
#                                     parse_mode=ParseMode.MARKDOWN_V2, text=msg_str)
        elif (context.args[1].isdigit()):
            update_id = int(context.args[1])
            if (update_id >= len(ddl_list)):
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text="ERROR: Id is not existed! " + str(update_id) + " .\n")
            else:
                Exc = False
                try:
                    update_datetime = datetime.datetime.fromisoformat(
                        context.args[3])
                except Exception:
                    Exc = True
                finally:
                    pass
                if (Exc == False and context.args[2] == "deadline"):
                    # print(type(ddl_list[0]))
                    if update_datetime.tzinfo == None:
                        update_datetime = datetime.datetime.fromisoformat(
                            update_datetime.isoformat()+"+08:00")
                    temp = ddl_list[update_id]
                    temp[context.args[2]] = update_datetime.isoformat()
                    context.bot.send_message(
                        chat_id=update.effective_chat.id, text="Updated " + temp['todo'] + " " + update_datetime.isoformat() + " !\n")
                    # print(ddl_list)
                    save_json(src=ddl_list)
                else:
                    context.bot.send_message(
                        chat_id=update.effective_chat.id, text=("ERROR: Invalid isoformat string!" + context.args[3]))
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="ERROR: Id is invilid! " + context.args[1] + " \n")
#        context.bot.send_message(chat_id=update.effective_chat.id,
#                                 parse_mode=ParseMode.MARKDOWN_V2, text=get_ddl_msg(ddl_list))
    elif context.args[0] == "finish":
        # print("finish")
        if (len(context.args) != 2):
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="ERROR: 2 args expected but " + str(len(context.args)) + " received")
        elif (context.args[1].isdigit()):
            finish_id = int(context.args[1])
            if (finish_id >= len(ddl_list)):
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text="ERROR: Id is not existed! " + str(finish_id) + ' \n')
            else:
                finish_item = ddl_list[finish_id]
                # context.bot.send_message(
                #    chat_id=update.effective_chat_id, text="Remove " + ddl_list[finish_id])
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text="Remove " + finish_item['deadline'] + " " + finish_item['todo'] + "\n")
                ddl_list.pop(finish_id)
                save_json(src=ddl_list)
                # TODO:增加二次确认
                # if confirm_str.strip() == "yes":
                #    ddl_list.pop(finish_id)
                #    save_json(src=ddl_list)
                # else:
                #    print(
                #        "Remove " + finish_item['deadline'] + " " + finish_item['todo'] + " (yes/other)\n")

    else:
        with open("./Help/ddl.md", "r") as f:
            context.bot.send_message(
                chat_id=update.effective_chat.id, parse_mode=ParseMode.MARKDOWN_V2, text=f.read())


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
