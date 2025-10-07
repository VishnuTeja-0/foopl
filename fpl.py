import requests
import utility.constants as constants
from datetime import datetime, timezone, timedelta
import asyncio
import traceback

_selected_timezones = {
    "IST" : timezone(timedelta(hours=5, minutes=30)), 
    "BST" : timezone(timedelta(hours=1, minutes=0))
}
_current_date = datetime.now(timezone.utc)
_deadline = None
_gameweek = 0
_message = "TEAMS SET KARLO AAJ {IST} / {BST} deadline\n{FLAGS}"
_is_playerwatch = True
_playerwatch_league_codes = [40804]
_flagged_players = {}


def authFpl():
    session = requests.session()
    fpl_url = constants.FPL_LOGIN
    data = {
        'password': '<pass>',
        'login': '<email>',
        'redirect_uri': 'https://fantasy.premierleague.com/a/login',
        'app': 'plfpl-web'
    } 
    session.post(fpl_url, data=data)
    return session

def getTimezoneDateObject(dt, tz = timezone.utc):
    if isinstance(dt, datetime):
        return dt.astimezone(tz)
    else:
        return datetime.fromisoformat(dt.replace("Z", "+00:00")).astimezone(tz)

async def saveDeadline():
    global _deadline, _current_date, _gameweek
    info_url = constants.FPL_BASIC
    try:
        response = requests.get(info_url)
        if response.status_code == 200:
            res = response.json()
            gameweek_deadline_values = [event["deadline_time"] for event in res["events"]]
            event_index, next_deadline = next(
                (i, dt)
                for i, date_string in enumerate(gameweek_deadline_values) 
                if _current_date < (dt := getTimezoneDateObject(date_string))
            )
            _deadline = next_deadline
            _gameweek = event_index + 1          
        else:
            raise Exception("Deadline fetch - request failed")
    except Exception as ex:
        # Error Logging
        print("Unable to get set deadline")
        print(ex.args, traceback.format_exc())
        return constants.DEADLINE_ERR
    
    
async def saveFlaggedPlayers():
    global _is_playerwatch, _playerwatch_league_codes, _flagged_players, _gameweek
    if _is_playerwatch:
        try:      
            user_ids = []
            for league_code in _playerwatch_league_codes:
                league_url = constants.FPL_LEAGUE.format(code = league_code)
                response = requests.get(league_url)
                if response.status_code == 200:
                    res = response.json()
                    standings = res["standings"]
                    do = True
                    while (do or standings["has_next"]):
                        user_ids.extend([user["entry"] for user in standings["results"]])
                        do = False
                else:
                    raise Exception("League users fetch - request failed")
                
            players = []
            teams=[]
            fpl_url = constants.FPL_BASIC
            response = requests.get(fpl_url)
            if response.status_code == 200:
                res = response.json()
                players.extend(res["elements"])
                teams.extend(res["teams"])
            else:
                raise Exception("Players and teams fetch - request failed")
            
            for id in user_ids:
                event = _gameweek - 1
                user_url = constants.FPL_USER_TEAM.format(manager_id = id, event = event)
                response = requests.get(user_url)
                if response.status_code == 200:
                    res = response.json()
                    player_pick_ids = [pick["element"] for pick in res["picks"]]
                    for id in player_pick_ids:
                        player_name, player_chance, team_code = next(
                            (p["web_name"], p["chance_of_playing_next_round"], p["team_code"])
                                for p in players
                                if p["id"] == id
                        )
                        if player_chance is not None and player_chance < 100 and player_name not in _flagged_players:
                            team_name = next(t["short_name"] for t in teams if t["code"] == team_code)
                            flagged_player = f"{player_name} ({team_name})"
                            _flagged_players[flagged_player] = player_chance
                else:
                    raise Exception("Flagged player fetch - request failed")
        except Exception as ex:
            # Error logging
            print("Unable to fetch flagged players")
            print(ex.args, traceback.format_exc())
            return constants.FLAGGED_ERR

def saveDeadlineMessage():
    global _deadline, _selected_timezones, _message
    try:
        times = {}
        if isinstance(_deadline, datetime):
            for key, value in _selected_timezones.items():
                nd_value_formatted = (ld := getTimezoneDateObject(_deadline, value)).strftime("%I:%M %p" if ld.minute > 0 else "%I %p")
                times[key] = nd_value_formatted + " " + key

            if _is_playerwatch:
                red_flags = []
                orange_flags = []
                yellow_flags = []
                for player, chance in _flagged_players.items():
                    if chance >= 75:
                        yellow_flags.append(player)
                    elif chance > 0:
                        orange_flags.append(player)
                    else:
                        red_flags.append(player)
                red = f"\n:red_square: {','.join(red_flags)}" if len(red_flags) > 0 else ""
                orange = f"\n:orange_square: {','.join(orange_flags)}" if len(orange_flags) > 0 else "" 
                yellow = f"\n:yellow_square: {','.join(yellow_flags)}" if len(yellow_flags) > 0 else ""         
                flagged_message = f"{red}{orange}{yellow}"
                times["FLAGS"] = flagged_message
            
            _message = _message.format(**times)
        else:
            raise Exception("Deadline not available")
    except Exception as ex:
        # Error Logging
        print("Unable to format message")
        print(ex.args, traceback.format_exc())
        return constants.DEADLINE_ERR
    
async def main():
    await saveDeadline()
    await saveFlaggedPlayers()
    saveDeadlineMessage()
    print(_message)

asyncio.run(main())