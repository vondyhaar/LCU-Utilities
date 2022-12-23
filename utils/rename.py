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

    def check_name(self, name) -> bool:
        r = self.lcu_api.request("GET", f"/lol-summoner/v1/check-name-availability/{name}")
        if r.status_code != 200:
            return False
        return r.json()

    def snipe(self, name):
        i = 0
        t_0 = time.time()
        try:
            r = False
            while not r:
                r = self.check_name(name)
                print(r)
                i += 1
                print(i)
                pass
            self.change_name(name)
        except:
            print(i)
            f = time.time() - t_0
            print(f"{f} s")
            print((f"{(i/f)} r/s" if i/f > 1 else f"{f/i} s/r"))
       
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


__instance = Rename()
check_name = __instance.check_name
change_name = __instance.change_name
get_new = __instance.get_new
snipe = __instance.snipe
