import requests

from discord_message import Message

headers = {'Content-type': 'application/json'}
link = "https://discord.com/api/webhooks/1017290951024185425/FiZ5otnZ5hxOtCUMX1LS7vuVCzKK3JklSo61s3Wp74EI7hu4Bbn2yGepe860u84aocdq?wait=true"
msg = Message()

r = requests.post(link, data=msg, headers=headers)
print(r.status_code)
print(r.json())