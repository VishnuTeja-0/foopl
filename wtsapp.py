import requests
import utility.constants as constants
from fpl import getDeadlineMessage

class Group:
    def __init__(self, id, name):
        self.name = name
        self.id = id

def getGroups():
    url = constants.WA_GET_GROUPS
    groups = []
    resMsg = "";
    try:
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()["results"]["data"]
            for group in result:
                groups.append(Group(group["JID"], group["Name"]))
            resMsg = "Fetched groups"

    except:
        # Error Logging
        resMsg = constants.WA_GET_GROUPS

    return groups
            
def sendMessage(contactId):
    url = constants.WA_SEND_MESSAGE
    message = getDeadlineMessage()
    try:
        response = requests.post(
            url,
            {
                "message" : message,
                "phone": contactId
            }
        )
        if response.status_code == 200:
            print("Message Sent")
    except:
        #Error Logging
        print("There was an error in sending message")
    



