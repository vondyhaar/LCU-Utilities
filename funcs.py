from api import RiotClientApi, LcuApi
import webbrowser


api = RiotClientApi()
lcu_api = LcuApi()


def match_phase(phase):
    r = lcu_api.request("GET", "/lol-gameflow/v1/gameflow-phase")
    if r.status_code != 200:
        return
    r = r.json()
    return True if r == phase else False


def dodge():
    r = lcu_api.request(
        "post",
        '/lol-login/v1/session/invoke?destination=lcdsServiceProxy&method=call&args=["","teambuilder-draft","quitV2",""]',
    )
    if r.status_code != 200:
        return


def get_names():
    r = api.request("GET", "/chat/v5/participants/champ-select")
    if r.status_code != 200:
        exit()
    r = r.json()
    participants = []
    for e in r["participants"]:
        participants.append(e["name"])
    return participants


def search():
    participants = get_names()
    if participants:
        url = f"https://porofessor.gg/pregame/{api.region.lower()}/{','.join(participants)}"
        webbrowser.open(url)
    else:
        participants = "No players found!"
    return participants
