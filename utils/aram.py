# utils/aram.py

from apis import *
import json
import time
import base64


class AramBoost:
    def __init__(self) -> None:
        self.lcu_api = LcuApi()
        self.data = {}
        try:
            with open("jwt.json") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            with open("jwt.json", "w") as f:
                json.dump(self.data, f)

    def get_jwt(self) -> None:
        self.jwt: str = self.lcu_api.request("GET", "/lol-inventory/v1/signedWallet/RP").json()["RP"]
        payload = self.jwt.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        payload = base64.b64decode(payload).decode("ascii")
        payload = json.loads(payload)
        rp = payload["balances"]["RP"]
        self.puuid = payload["sub"]
        if rp >= 95:
            self.exp = payload["exp"]
            self.data.update(
                {
                    self.puuid: {
                        "jwt": self.jwt,
                        "exp": self.exp,
                    }
                }
            )
            with open("jwt.json", "w") as f:
                json.dump(self.data, f, indent=4)
            return "Successfully got new JWT value"
        else:
            with open("jwt.json") as f:
                data: dict = json.load(f)
            user = data.get(self.puuid)
            if user is None:
                return "No JWT value for this user!"
            if time.time() > user["exp"]:
                return "Previous JWT value is too old!"
            self.jwt = user["jwt"]
            self.exp = user["exp"]
            return "Successful fallback to previous JWT value"

    def boost(self) -> None:
        r = self.lcu_api.request("GET", "/lol-gameflow/v1/gameflow-phase").json()
        if r != "ChampSelect":
            return
        if time.time() > self.exp:
            return "Expired"
        rp = self.lcu_api.request("GET", "/lol-store/v1/wallet").json()["rp"]
        if rp >= 95:
            return
        r = self.lcu_api.request(
            "POST",
            f'/lol-login/v1/session/invoke?destination=lcdsServiceProxy&method=call&args=["","teambuilder-draft","activateBattleBoostV1","{{\\"signedWalletJwt\\":\\"{self.jwt}\\"}}"]',
        )


__instance = AramBoost()
get_jwt = __instance.get_jwt
boost = __instance.boost
