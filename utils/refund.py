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

    def refund(self, id):
        body = {"accountId": self.account_id, "transactionId": id}
        r = self.storefront_api.request("POST", "/storefront/v3/refund", body)
        if r.status_code != 200:
            return r.json()
        return True

    def update_transactions(self) -> None:
        r = self.storefront_api.request("GET", "/storefront/v3/history/purchase")
        if r.status_code != 200:
            return
        r = r.json()

        self.transactions = {}
        print(r["transactions"])
        for e in r["transactions"]:
            if (
                e.get("refundabilityMessage")
                in [
                    "ALREADY_REFUNDED",
                    "NON_REFUNDABLE_INVENTORY_TYPE",
                    "FREE_OR_REWARDED_ITEM",
                ]
                or e.get("requiresToken") != False
            ):
                continue

            self.transactions.update({self.catalog.get(str(e["itemId"])): e})

    def get_transactions(self) -> dict:
        return self.transactions

    def get_transaction(self, key) -> dict:
        return self.transactions.get(key)


__instance = Refund()
refund = __instance.refund
update_transactions = __instance.update_transactions
get_transactions = __instance.get_transactions
get_transaction = __instance.get_transaction
