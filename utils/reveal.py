# utils/reveal.py

from apis import *
import webbrowser


class RevealNames:
    lcu_api = LcuApi()
    riot_api = RiotClientApi()

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
            exit()
        r = r.json()
        participants = []
        for e in r["participants"]:
            participants.append(e["name"])
        return participants if participants else "No players found!"

    def search(self) -> None:
        participants = self.get_names()
        if isinstance(participants, str) or len(participants) == 1:
            return
        url = f"https://porofessor.gg/pregame/{self.lcu_api.region.lower()}/{','.join(participants)}"
        webbrowser.open(url)


__instance = RevealNames()
match_phase = __instance.match_phase
dodge = __instance.dodge
get_names = __instance.get_names
search = __instance.search
