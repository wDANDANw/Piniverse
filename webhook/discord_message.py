import json

class MsgParams:

    def __init__(self):
        self.creator = "Piniverse"
        self.title = "Title"
        self.description = "Text message. You can use Markdown here. *Italic* **bold** __underline__ ~~strikeout~~ [hyperlink](https://google.com) `code`"
        self.url = ""
        self.noti_type = "Default Notification Type"
        self.noti_info_title = "Default Notification Info Title"
        self.noti_info_content = "Default Notification Info Content"
        self.color = 15258703
        self.location = "Default Location"
        self.footer = "Piniverse Bot · Time"

    def getNotiType(self, kwargs):

        if not kwargs: # Dict is empty
            return "Default Notification Type"
        elif kwargs["ntype"] == "assigned":
            return "New Assigned Task"

    def getNotiInfoTitle(self, kwargs):

        if not kwargs: # Dict is empty
            return "Default Notification Info Title"
        elif kwargs["ntype"] == "assigned":
            return "Due Date"

    def getNotiInfoContent(self, kwargs, due_date):
        
        if not kwargs: # Dict is empty
            return "Default Notification Info Content"
        elif kwargs["ntype"] == "assigned":   
            if not due_date:
                return "N/A"
            else:
                return "Due by {}".format(due_date)


def GetDefaultMsgParams():
    return MsgParams();

def Message(params = GetDefaultMsgParams()):

    # Dict for the json
    msg = {
        "username": "Piniverse Bot",
        "avatar_url": "https://i.imgur.com/4M34hi2.png",
        "embeds": [
            {
            "author": {
                "name": params.creator,
                "url": "",
                "icon_url": "https://i.imgur.com/R66g1Pe.jpg"
            },
            "title": params.title,
            "url": params.url,
            "description": params.description,
            "color": params.color,
            "fields": [
                {
                "name": "Notification Type",
                "value": params.noti_type,
                "inline": True
                },
                {
                "name": params.noti_info_title,
                "value": params.noti_info_content,
                "inline": True
                },
                {
                "name": "\nLocation",
                "value": params.location
                },
            ],
            # "thumbnail": {
            #     "url": "https://upload.wikimedia.org/wikipedia/commons/3/38/4-Nature-Wallpapers-2014-1_ukaavUI.jpg"
            # },
            # "image": {
            #     "url": "https://upload.wikimedia.org/wikipedia/commons/5/5a/A_picture_from_China_every_day_108.jpg"
            # },
            "footer": {
                "text": params.footer,
                "icon_url": "https://i.imgur.com/fKL31aD.jpg"
            }
            }
        ]
    }

    # return
    return json.dumps(msg)