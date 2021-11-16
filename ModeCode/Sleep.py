import json
import LoadConf
from telegram import update,ParseMode
from telegram.ext import Updater

updater = Updater(token=LoadConf.conf['bot']['token'], use_context=True)
bot = updater.bot

with open("./Logs/TimeAsleep.json", "r", newline="", encoding="utf-8") as f:
    TimeAsleep = json.load(f)

with open("./Logs/SleepRings.json", "r", newline="", encoding="utf-8") as f:
    SleepRings = json.load(f)

msg = "早上好，昨晚睡得如何，下面是您昨晚的睡眠监测数据\n昨夜睡眠质量总体评价是*"+SleepRings['SleepRating']+"*\n"

msg += ("睡眠时间从 "+TimeAsleep['Start']+" 直到 " +
        TimeAsleep['Until']+" 睡眠时间为 " + TimeAsleep['Sleep'] + "h，达到睡眠目标的"+SleepRings["Sleep%"]+'%\n')

msg += "\n睡眠银行是autosleep用算法推测的衡量所需睡眠时间和实际睡眠时间的比值，应该保持为正数您白天才会更加健康和精神\n"
if float(TimeAsleep['Credit%']) > 0:
    msg += ("您当前睡眠银行信用值: " + TimeAsleep['Credit%'] + "% 继续保持哟 ^_^\n")
if float(TimeAsleep['Debt%']) > 0:
    msg += ("*您当前睡眠银行负债为: " + TimeAsleep['Debt%'] + "%* 多休息一下，别累坏身子鸭 ^_^\n")

msg += ("深度睡眠时间: " + SleepRings['Deep'] +
        "h ，达到目标的 " + SleepRings['Deep%'] + "% \n")

msg += "\nbpm是心率沉浸，是睡眠心率平均值与非活动日间心率平均值的下降值，10%或更高是健康睡眠的重要指标\n"
bpm = float(SleepRings['bpm%'])/10.0
msg += ("bpm: " + str(bpm) + "%  \n")

msg = msg.replace(".","\.")
msg = msg.replace("_","\_")

# print(TimeAsleep)
# print(SleepRings)
print(msg)

bot.send_message(chat_id=LoadConf.conf['bot']['sleepinfo_id'],
                     parse_mode=ParseMode.MARKDOWN_V2, text=msg)