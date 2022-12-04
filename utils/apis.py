# utils/apis.py

import urllib3
from requests.auth import HTTPBasicAuth
import psutil
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_args():
    for e in psutil.process_iter():
        if e.name() in ["LeagueClientUx", "LeagueClientUx.exe"]:
            lcu_process = e
            break
    else:
        exit()

    process_args = {}
    for e in lcu_process.cmdline():
        if "=" in e:
            key, value = e[2:].split("=", 1)
            process_args.update({key: value})
    return process_args


process_args = get_args()


class RiotClientApi:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(__class__, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.port = process_args.get("riotclient-app-port")
        self.auth = HTTPBasicAuth("riot", process_args.get("riotclient-auth-token"))

    def request(self, method, endpoint, json=None):
        return requests.request(
            method=method, url=f"https://127.0.0.1:{self.port}{endpoint}", verify=False, auth=self.auth, json=json
        )


class LcuApi:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(__class__, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.region = process_args.get("region")
        self.port = process_args.get("app-port")
        self.auth = HTTPBasicAuth("riot", process_args.get("remoting-auth-token"))

    def request(self, method, endpoint, json=None):
        return requests.request(
            method, f"https://127.0.0.1:{self.port}{endpoint}", verify=False, auth=self.auth, json=json
        )


class StorefrontApi:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(__class__, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        lcu_api = LcuApi()
        r = lcu_api.request("GET", "/lol-login/v1/session").json()
        self.token = r["idToken"]
        self.region = lcu_api.region

    def request(self, method, endpoint, json=None):
        return requests.request(
            method,
            f"https://{self.region}.store.leagueoflegends.com{endpoint}",
            json=json,
            headers={"Authorization": f"Bearer {self.token}"},
        )
