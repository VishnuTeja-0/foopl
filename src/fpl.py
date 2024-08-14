import requests
import utility.constants as constants
from datetime import datetime, timezone, timedelta

ist_timezone = timezone(timedelta(hours=5, minutes=30))

def authFpl():
    session = requests.session()
    fpl_url = constants.LOGIN_URL
    data = {
        'password': '<YOUR PASSWORD>',
        'login': '<YOUR EMAIL>',
        'redirect_uri': 'https://fantasy.premierleague.com/a/login',
        'app': 'plfpl-web'
    }
    
    session.post(fpl_url, data=data)
    return session

def getISTDateObject(date_string):
    return datetime.fromisoformat(date_string.replace("Z", "+00:00")).astimezone(ist_timezone)

def getDeadline():
    ist_timezone = timezone(timedelta(hours=5, minutes=30))
    current_date = datetime.now(timezone.utc).astimezone(ist_timezone)
    info_url = constants.FPL_BASIC
    try:
        response = requests.get(info_url)
        if response.status_code == 200:
            res = response.json()
            gameweek_deadline_values = [event["deadline_time"] for event in res["events"]]
            next_deadline = next(getISTDateObject(date_string) for date_string in gameweek_deadline_values 
                            if current_date < getISTDateObject(date_string))
            
            return next_deadline
            
        else:
            return None
    except(Exception):
        # Error Logging
        print("Error in fetching FPL")
        return None
    
def formatMessage():
    deadline = getDeadline()
    if isinstance(deadline, datetime):
        nd_value_formatted = deadline.strftime("%I:%M %p" if deadline.minute > 0 else "%I %p")
        message = "Teams set karlo deadline aaj " + nd_value_formatted + " baje hai"
        print(message)
    else:
        print("Error")

