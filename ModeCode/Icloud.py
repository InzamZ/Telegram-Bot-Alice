import json
import pyicloud

icloudapi = pyicloud.PyiCloudService('3028891035@qq.com')
print(icloudapi.drive.dir())

f = icloudapi.drive['Telegram-Bot-Alice']['sleep.json']
from shutil import copyfileobj
with f.open(stream=True) as response:
    with open(f.name, 'wb') as file_out:
        copyfileobj(response.raw, file_out)
        sleepinfo = str()
        file_out.write(sleepinfo)

