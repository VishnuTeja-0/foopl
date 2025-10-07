# API URLs
FPL_LOGIN = "https://users.premierleague.com/accounts/login/"
FPL_BASIC = "https://fantasy.premierleague.com/api/bootstrap-static/"
FPL_LEAGUE = "https://fantasy.premierleague.com/api/leagues-classic/{code}/standings/"
FPL_USER_TEAM = "https://fantasy.premierleague.com/api/entry/{manager_id}/event/{event}/picks/"

WA_GET_GROUPS = "http://localhost:3000/user/my/groups"
WA_SEND_MESSAGE = "http://localhost:3000/send/message"

# Error Messages
DEADLINE_ERR = "There was an error in fetching the gameweek deadline"
FLAGGED_ERR = "There was an error in fetching flagged players"
GROUPS_ERR = "There was an error in fetching your groups"
SEND_MESSAGE_ERR = "There was an error in sending message"

# Config Values
WA_COUNTRY_EXCEPTIONS = {86, 98, 963, 850, 979}