# utils/aram.py

from enum import Enum
from apis import *
import json
import time
import base64


class AramBoost:
    def __init__(self) -> None:
        self.lcu_api = LcuApi()
        self.data = {}
        self.get_jwt()
        try:
            with open("jwt.json") as f:
                self.data = json.load(f)
                from_file = self.data.get(self.puuid).get("lastUse") if self.data.get(self.puuid) != None else None
                self.last_use = 0 if (from_file is None) else from_file
        except FileNotFoundError:
            with open("jwt.json", "w") as f:
                json.dump(self.data, f)

    def get_jwt(self) -> str:
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
                return "JWT value is too old!"
            self.jwt = user["jwt"]
            self.exp = user["exp"]
            return "Successful fallback to previous JWT value"

    def get_last_use(self) -> float:
        return int(self.last_use)

    def boost(self) -> int:
        if time.time() > self.exp:
            return 3
        rp = self.lcu_api.request("GET", "/lol-store/v1/wallet").json()["rp"]
        if rp >= 95:
            return 2
        r = self.lcu_api.request(
            "POST",
            f'/lol-login/v1/session/invoke?destination=lcdsServiceProxy&method=call&args=["","teambuilder-draft","activateBattleBoostV1","{{\\"signedWalletJwt\\":\\"{self.jwt}\\"}}"]',
        )
        self.last_use = time.time()
        with open("jwt.json", "r") as f:
            data = json.load(f)
            self.last_use = time.time()
            data[self.puuid].update({"lastUse": self.last_use})
            with open("jwt.json", "w") as w:
                json.dump(data, w, indent=4)
        return 1


__instance = AramBoost()
get_jwt = __instance.get_jwt
get_last_use = __instance.get_last_use
boost = __instance.boost
