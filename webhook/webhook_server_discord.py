import time
import webhook_listener
import cherrypy
import json
import requests

from datetime import datetime
import pytz

from discord_message import Message, MsgParams

headers = {'Content-type': 'application/json'}
link = "https://discord.com/api/webhooks/1017290951024185425/FiZ5otnZ5hxOtCUMX1LS7vuVCzKK3JklSo61s3Wp74EI7hu4Bbn2yGepe860u84aocdq?wait=true"

def process_post_request(request, *args, **kwargs):
    
    body = request.body.read(int(request.headers["Content-Length"])) if int(request.headers.get("Content-Length", 0)) > 0 else ""
    body = json.loads(body.decode('utf-8'))

    print(kwargs)

    params = MsgParams()
    params.creator = "Piniverse"
    params.description = body["payload"]["description"]
    params.title = body["payload"]["name"]
    params.url = body["payload"]["url"]
    params.noti_type = params.getNotiType(kwargs).ljust(24) # Pad to 24 letters
    params.noti_info_title = params.getNotiInfoTitle(kwargs).ljust(24)
    params.noti_info_content = params.getNotiInfoContent(kwargs, body["payload"]["due_date"]).ljust(24)
    params.color = 15258703
    params.location = "[{}](https://google.com)".format(body["payload"]["folder"]["name"])
    params.footer = "Piniverse Bot · Time {}".format(datetime.now(pytz.timezone('America/New_York')).strftime('%Y-%m-%d %H:%M'))

    r = requests.post(link, data=Message(params), headers=headers)
    print(r.status_code)
    print(r.json())

    return


webhooks = webhook_listener.Listener(handlers={"POST": process_post_request})
webhooks.start()

while True:
    print("Still alive...")
    time.sleep(300)