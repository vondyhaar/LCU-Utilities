# utils/aram.py

from apis import *
import json
import datetime as dt


class AramBoost:
    def __init__(self) -> None:
        self.lcu_api = LcuApi()
        self.data = {}
        self.summoner_id = self.lcu_api.request(
            "GET", "/lol-summoner/v1/current-summoner/account-and-summoner-ids"
        ).json()["summonerId"]
        try:
            with open("jwt.json") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            with open("jwt.json", "w") as f:
                json.dump(self.data, f)

    def get_jwt(self) -> None:
        rp = self.lcu_api.request("GET", "/lol-store/v1/wallet").json()["rp"]
        if rp >= 95:
            self.jwt = self.lcu_api.request("GET", "/lol-inventory/v1/signedWallet/RP").json()["RP"]
            self.data.update(
                {
                    str(self.summoner_id): {
                        "latest_jwt": self.jwt,
                        "date": dt.datetime.now().strftime("%H:%M:%S %d-%b-%Y"),
                    }
                }
            )
            with open("jwt.json", "w") as f:
                json.dump(self.data, f, indent=4)
            return "Successfully got new JWT value"
        with open("jwt.json") as f:
            data: dict = json.load(f)
        user = data.get(str(self.summoner_id))
        if user is None:
            return "No JWT value for this user!"
        if (dt.datetime.now() - dt.datetime.strptime(user["date"], "%H:%M:%S %d-%b-%Y")) > dt.timedelta(days=1):
            return "Previous JWT value is too old!"
        self.jwt = user["latest_jwt"]
        return "Successful fallback to previous JWT value"

    def boost(self) -> None:
        r = self.lcu_api.request("GET", "/lol-gameflow/v1/gameflow-phase").json()
        if r != "ChampSelect":
            return
        rp = self.lcu_api.request("GET", "/lol-store/v1/wallet").json()["rp"]
        if rp < 95:
            r = self.lcu_api.request(
                "POST",
                f'/lol-login/v1/session/invoke?destination=lcdsServiceProxy&method=call&args=["","teambuilder-draft","activateBattleBoostV1","{{\\"signedWalletJwt\\":\\"{self.jwt}\\"}}"]',
            )


__instance = AramBoost()
get_jwt = __instance.get_jwt
boost = __instance.boost
