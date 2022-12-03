# aram.py

from apis import *


class AramBoost:
    jwt = ""
    lcu_api = LcuApi()

    def __init__(self) -> None:
        rp = self.lcu_api.request("GET", "/lol-store/v1/wallet").json()["rp"]
        if rp >= 95:
            self.jwt = self.lcu_api.request("GET", "/lol-inventory/v1/signedWallet/RP").json()["RP"]

    def get_jwt(self) -> None:
        rp = self.lcu_api.request("GET", "/lol-store/v1/wallet").json()["rp"]
        if rp >= 95:
            self.jwt = self.lcu_api.request("GET", "/lol-inventory/v1/signedWallet/RP").json()["RP"]
            print("refreshed")

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
