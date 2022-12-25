# utils/reveal.py

from apis import *
import webbrowser


class RevealNames:
    def __init__(self) -> None:
        self.lcu_api = LcuApi()
        self.riot_api = RiotClientApi()

    def match_phase(self, phase) -> bool:
        r = self.lcu_api.request("GET", "/lol-gameflow/v1/gameflow-phase")
        if r.status_code != 200:
            return
        r = r.json()
        return True if r == phase else False

    def dodge(self) -> None:
        r = self.lcu_api.request(
            "post",
            '/lol-login/v1/session/invoke?destination=lcdsServiceProxy&method=call&args=["","teambuilder-draft","quitV2",""]',
        )
        if r.status_code != 200:
            pass

    def get_names(self) -> str | list:
        r = self.riot_api.request("GET", "/chat/v5/participants/champ-select")
        if r.status_code != 200:
            return "Error"
        r = r.json()
        participants = []
        for e in r["participants"]:
            participants.append(e["name"])
        return participants if participants else "No players found!"

    def search(self, option) -> None:
        participants = self.get_names()
        if isinstance(participants, str) or len(participants) == 1:
            return
        match option:
            case "OPGG":
                url = f"https://www.op.gg/multisearch/{self.lcu_api.region.lower()}?summoners={','.join(participants)}"
            case "Porofessor":
                url = f"https://porofessor.gg/pregame/{self.lcu_api.region.lower()}/{','.join(participants)}"
            case "U.GG":
                url = f"https://u.gg/multisearch?summoners={','.join(participants)}&region={self.lcu_api.region.lower()}"
        webbrowser.open(url)


__instance = RevealNames()
match_phase = __instance.match_phase
dodge = __instance.dodge
get_names = __instance.get_names
search = __instance.search
