# utils/refund.py

from apis import *


class Refund:
    def __init__(self) -> None:
        self.storefront_api = StorefrontApi()
        r = self.storefront_api.request("GET", "/storefront/v3/view/skins?language=en_US")
        if r.status_code != 200:
            return
        r = r.json()

        self.catalog = {}
        for e in r["catalog"]:
            if e["inventoryType"] == "BUNDLES":
                continue
            self.catalog.update({str(e["itemId"]): e["name"]})

        self.account_id = self.storefront_api.request("GET", "/storefront/v3/featured?language=en_US").json()[
            "player"
        ]["accountId"]

        self.update_transactions()

    def refund(self, key) -> None:
        t = self.transactions.get(key)
        if t is None:
            return
        json = {"accountId": self.account_id, "transactionId": t["transactionId"]}
        r = self.storefront_api.request("POST", "/storefront/v3/refund", json)
        if r.status_code == 200:
            self.transactions.pop(key, None)


    def update_transactions(self) -> None:
        r = self.storefront_api.request("GET", "/storefront/v3/history/purchase")
        if r.status_code != 200:
            return
        r = r.json()

        self.transactions = {}
        for e in r["transactions"]:
            if e["refundable"] != True:
                continue
            self.transactions.update({self.catalog.get(str(e["itemId"])): e})

    def get_transactions(self) -> dict:
        return self.transactions


__instance = Refund()
refund = __instance.refund
update_transactions = __instance.update_transactions
get_transactions = __instance.get_transactions
