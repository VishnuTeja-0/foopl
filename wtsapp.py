import requests
import utility.constants as constants
from fpl import getDeadlineMessage
from phonenumbers import COUNTRY_CODE_TO_REGION_CODE as phonecode
from pycountry import countries
import re
import emoji

class Group:
    def __init__(self, id, name):
        self.name = name
        self.id = id

_nonbmp = re.compile(r'[\U00010000-\U0010FFFF]')

def _encodeNonBmp(match):
    char = match.group()
    assert ord(char) > 0xffff
    if emoji.is_emoji(char):
        demoji = emoji.demojize(char)
        return " " + demoji + " "
    else:
        return "--"

def replaceNonBmp(text):
    return _nonbmp.sub(_encodeNonBmp, text)

def getGroups():
    url = constants.WA_GET_GROUPS
    groups = []
    resMsg = "";
    try:
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()["results"]["data"]
            for group in result:
                groups.append(Group(group["JID"], replaceNonBmp(group["Name"])))
            resMsg = "Fetched groups"

    except:
        # Error Logging
        resMsg = constants.WA_GET_GROUPS

    return (groups,resMsg)
            
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

def getCountryCodeList():
    country_code_items = []
    
    for code, alpha_tuple in phonecode.items():
        if code not in constants.WA_COUNTRY_EXCEPTIONS and alpha_tuple[0] != '001':
            for alpha in alpha_tuple:
                code_item = ""
                country_data = countries.get(alpha_2 = alpha)
                if country_data is not None:
                    code_item += country_data.alpha_3
                else:
                    code_item += alpha
                
                code_item += " " + str(code)
                country_code_items.append(code_item)
    
    return country_code_items

# print([group.name for group in getGroups()[0]])
# print(getCountryCodeList())