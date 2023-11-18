import requests
from datetime import datetime

async def getGiveaways():
    giveaways = []
    date = datetime.now()
    msg = f'Game Giveaways:\n\n'

    response = requests.get('https://www.gamerpower.com/api/filter?platform=steam.epic-games-store.ubisoft.origin.switch.vr&sort-by=popularity&type=game')
    json = response.json()
    for game in json:
        msg += f"[{game['title']}]({game['gamerpower_url']})\n"
    giveaways.append(msg)
    return giveaways
