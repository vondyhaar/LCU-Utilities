# utils/rename.py

from apis import *
from psutil import process_iter
import time


class Rename:
    def __init__(self) -> None:
        self.lcu_api = LcuApi()
        self.storefront_api = StorefrontApi()

        self.account_id = self.lcu_api.request("GET", f"/lol-summoner/v1/current-summoner").json()["accountId"]
        self.is_new = self.lcu_api.request("GET", "/lol-login/v1/session").json()["isNewPlayer"]
        self.sniping = False

    def check_name(self, name) -> bool:
        r = self.lcu_api.request("GET", f"/lol-summoner/v1/check-name-availability/{name}")
        if r.status_code != 200:
            return False
        return r.json()

    def snipe(self, name):
        i = 0
        t_0 = time.time()
        r = False
        while not r and self.sniping:
            r = self.check_name(name)
            i += 1
            pass
        t = time.time() - t_0
        info: str = f"{i} requests\n" + (f"{round(i/t, 4)} r/s" if i / t > 1 else f"{round(t/i, 4)} s/r") + "\n"
        if r:
            self.change_name(name)
        return info

    def change_name(self, name) -> None:
        if self.is_new:
            r = self.lcu_api.request("post", "/lol-summoner/v1/summoners", {"name": name})
            if r.status_code == 200:
                for e in process_iter():
                    if e.name() in ["LeagueClientUxRender", "LeagueClientUxRender.exe"]:
                        e.kill()
            return r.json()

        data = {
            "summonerName": name,
            "accountId": self.account_id,
            "items": [
                {
                    "inventoryType": "SUMMONER_CUSTOMIZATION",
                    "itemId": 1,
                    "ipCost": 13900,
                    "rpCost": "null",
                    "quantity": 1,
                }
            ],
        }
        r = self.storefront_api.request("post", "/storefront/v3/summonerNameChange/purchase", data)
        return r.json()

    def get_new(self):
        return self.is_new

    def toggle_snipe(self):
        self.sniping = not self.sniping


__instance = Rename()
check_name = __instance.check_name
change_name = __instance.change_name
get_new = __instance.get_new
snipe = __instance.snipe
toggle_snipe = __instance.toggle_snipe
