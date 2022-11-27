from api import RiotClientApi
import webbrowser

api = RiotClientApi()
r = api.request("GET", "/chat/v5/participants/champ-select")
if r.status_code != 200:
    exit()
r = r.json()
if r["participants"]:
    participants = []
    for e in r["participants"]:
        participants.append(e["name"])
    url = (f"https://porofessor.gg/pregame/{api.region.lower()}/{','.join(participants)}")
    webbrowser.open(url)
else:
    print("No players found!")