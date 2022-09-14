from collections import UserList
import json
from typing import List, Tuple
import pytz
import requests
from telegram import Update, constants, Chat
from telegram.ext import CommandHandler, ContextTypes
from datetime import datetime

proxy = '127.0.0.1:7890'
proxies = {
    'http': 'http://' + proxy,
    'https': 'http://' + proxy,
}


def GetUserList(CfgFilePath="./Data/CodeforcesPeekingTom.cfg")-> List:
    with open(CfgFilePath, "r", newline="", encoding="GBK") as f:
        userList = json.load(f)
    return userList


def UpdateUserList(userList, CfgFilePath="./Data/CodeforcesPeekingTom.cfg"):
    with open(CfgFilePath, "w", newline="", encoding="GBK") as f:
        f.write(json.dumps(userList, sort_keys=True, indent=4))


def GetStatusMsg(CfgFilePath="./Data/CodeforcesPeekingTom.cfg"):
    userList = GetUserList(CfgFilePath)
    r = requests.get(
        'https://codeforces.com/api/contest.list', proxies=proxies)
    ContestInfo = json.loads(r.text)["result"]
    ContestList = {}
    for x in ContestInfo:
        ContestList[x["id"]] = x

    RecentStatusList = []
    for user in userList:
        lastStatusId = user["lastStatusId"]
        r = requests.get('https://codeforces.com/api/user.status?handle=' +
                         user["handle"]+"&from=1&count=5", proxies=proxies)
        if r.status_code != 200:
            return -1
        Submissions = json.loads(r.text)["result"]
        for x in Submissions:
            user["lastStatusId"] = max(user["lastStatusId"], x["id"])
            if lastStatusId >= x["id"]:
                break
            RecentStatusList.append(x)
    '''
    RecentStatusListItemSample = {
        "id": 172002196, "contestId": 1729, "creationTimeSeconds": 1663053486, "relativeTimeSeconds": 1986,
        "problem": {
            "contestId": 1729,
            "index": "B",
            "name": "Decode String",
            "type": "PROGRAMMING",
            "tags": ["greedy", "strings"]
        }, 
        "author": {
            "contestId": 1729,
            "members": [{"handle": "lue"}],
            "participantType": "VIRTUAL",
            "ghost": false,
            "startTimeSeconds": 1663051500
        },
        "programmingLanguage": "Python 3", "verdict": "OK", "testset": "TESTS", 
        "passedTestCount": 6, "timeConsumedMillis": 420, "memoryConsumedBytes": 0
    }'''
    tz = pytz.timezone('Asia/Shanghai')
    ReplyMsg = ""
    for x in RecentStatusList:
        if ReplyMsg != "":
            ReplyMsg += '\n'
        TmpMsg = '<b>{UserHandle}</b> {creationTimeSeconds}提交了\n{ContestName} 的 <b>{ProblemIndex} - {ProblemName}</b>\n'.format(
            UserHandle=x["author"]["members"][0]["handle"],
            ProblemIndex=x["problem"]["index"],
            ProblemName=x["problem"]["name"],
            ContestName=ContestList[x["author"]["contestId"]]["name"],
            creationTimeSeconds=str(datetime.fromtimestamp(x["creationTimeSeconds"], tz))[:-6])
        try:
            TmpMsg += "Verdict: <b>{Verdict}</b>\n".format(
                Verdict=x["verdict"])
        except:
            pass
        try:
            # TmpMsg += "Testset: {Testset}".format(Testset=x["testset"])
            TmpMsg += "ProgrammingLanguage: {ProgrammingLanguage}\n".format(
                ProgrammingLanguage=x["programmingLanguage"])
        except:
            pass
        try:
            TmpMsg += "TimeConsumedMillis: {TimeConsumedMillis}\n".format(
                TimeConsumedMillis=x["timeConsumedMillis"])
            # TmpMsg += "MemoryConsumedBytes: {MemoryConsumedBytes}".format(MemoryConsumedBytes=x["memoryConsumedBytes"])
        except:
            pass
        ReplyMsg += TmpMsg
    UpdateUserList(userList)
    return ReplyMsg


async def PeekingYou(context: ContextTypes.DEFAULT_TYPE) -> int:
    job = context.job
    Msg = GetStatusMsg()
    if Msg != "":
        await context.bot.send_message(chat_id=job.chat_id,
                                       parse_mode=constants.ParseMode.HTML,
                                       text=Msg)


async def CodeforcesPeekingTomStart(update: Update,
                                    context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_message.chat_id
    jobTuple = context.job_queue.get_jobs_by_name(
        "CFPeekingTom" + str(chat_id))
    for job in jobTuple:
        job.schedule_removal()
    context.job_queue.run_repeating(
        PeekingYou, 300, chat_id=chat_id, name="CFPeekingTom" + str(chat_id))
    await context.bot.send_message(chat_id=chat_id, parse_mode=constants.ParseMode.HTML, text="I am peeking all of U , haha!")


async def CodeforcesPeekingTomStartChannelByName(update: Update,
                                                 context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_message.chat_id
    try:
        ChannelName = str(context.args[0])
        chat = await context.bot.get_chat(ChannelName)
        context.job_queue.run_repeating(
            PeekingYou, 300, chat_id=chat.id, name="CFPeekingTom" + str(chat_id))
        await context.bot.send_message(chat_id=chat.id, parse_mode=constants.ParseMode.HTML, text="I am peeking and send to Channel <b>{ChannelName}</b>, haha!".format(
            ChannelName=chat.title
        ))
    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /CFPeekingTomStartChannel <ChannelName>")


async def CodeforcesPeekingTomStartChannelById(update: Update,
                                               context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_message.chat_id
    try:
        ChannelId = int(context.args[0])
        chat = await context.bot.get_chat(ChannelId)
        context.job_queue.run_repeating(
            PeekingYou, 10, chat_id=chat.id, name="CFPeekingTom" + str(chat_id))
        await context.bot.send_message(chat_id=chat.id,
                                       parse_mode=constants.ParseMode.HTML,
                                       text="I am peeking and send to Channel <b>{ChannelName}</b>, haha!".format(
                                           ChannelName=chat.title
                                       ))
    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /CFPeekingTomStartChannel <ChannelId>")


async def CodeforcesPeekingTomAddUser(update: Update,
                                      context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_message.chat_id
    UserHandle = str(context.args[0])
    r = requests.get(
        'https://codeforces.com/api/user.info?handles=' + UserHandle, proxies=proxies)
    if r.status_code != 200:
        return -1
    user = json.loads(r.text)["result"][0]
    userList = GetUserList()
    for x in userList:
        if x["handle"] == user["handle"]:
            for k in user.keys():
                x[k] = user[k]
            UpdateUserList(userList)
            return 0
    user["lastStatusId"] = 1
    userList.append(user)
    UpdateUserList(userList)
    await context.bot.send_message(chat_id=chat_id, parse_mode=constants.ParseMode.HTML, text="I am peeking a new user <b>{UserHandle}</b>!".format(
        UserHandle = UserHandle
    ))

if "__main__" == __name__:
    print(GetStatusMsg(CfgFilePath="./Data/CodeforcesPeekingTom.cfg"))
