# utils/rename.py

from apis import *


class Rename:
    def __init__(self) -> None:
        self.lcu_api = LcuApi()
        self.storefront_api = StorefrontApi()

        self.account_id = self.lcu_api.request("GET", f"/lol-summoner/v1/current-summoner").json()["accountId"]
        self.is_new = self.lcu_api.request("GET", "/lol-login/v1/session").json()["isNewPlayer"]

    def check_name(self, name) -> bool:
        r = self.lcu_api.request("GET", f"/lol-summoner/v1/check-name-availability/{name}")
        if r.status_code != 200:
            exit()
        return r.json()

    def change_name(self, name) -> None:
        if self.is_new:
            r = self.lcu_api.request("post", "/lol-summoner/v1/summoners", {"name": name})
            if r.status_code == 200:
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


__instance = Rename()
check_name = __instance.check_name
change_name = __instance.change_name
