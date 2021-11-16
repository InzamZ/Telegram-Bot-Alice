import json
import Icloud

drive_file = Icloud.api.drive["Telegram-Bot-Alice"]["log"]["autosleep"]["Timesleep.json"]
from shutil import copyfileobj
with drive_file.open(stream=True) as response:
    with open(drive_file.name, 'wb') as file_out:
        copyfileobj(response.raw, file_out)
