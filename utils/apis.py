# utils/apis.py

import urllib3
from requests.auth import HTTPBasicAuth
import psutil
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_args():
    proc_list = list(psutil.process_iter())
    for e in proc_list:
        if e.name() in ["LeagueClientUx", "LeagueClientUx.exe"]:
            lcu_process = e
            break
    else:
        for e in proc_list:
            if e.name() in ["LeagueClient", "LeagueClient.exe"]:
                e.kill()
                break
        exit()

    process_args = {}
    for e in lcu_process.cmdline():
        if "=" in e:
            key, value = e[2:].split("=", 1)
            process_args.update({key: value})
    return process_args


process_args = get_args()


class RiotClientApi:
    port = process_args.get("riotclient-app-port")
    auth = HTTPBasicAuth("riot", process_args.get("riotclient-auth-token"))

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(__class__, cls).__new__(cls)
        return cls.instance

    def request(self, method, endpoint, json=None):
        return requests.request(
            method=method, url=f"https://127.0.0.1:{self.port}{endpoint}", verify=False, auth=self.auth, json=json
        )


class LcuApi:
    region = process_args.get("region")
    port = process_args.get("app-port")
    auth = HTTPBasicAuth("riot", process_args.get("remoting-auth-token"))

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(__class__, cls).__new__(cls)
        return cls.instance

    def request(self, method, endpoint, json=None):
        return requests.request(
            method, f"https://127.0.0.1:{self.port}{endpoint}", verify=False, auth=self.auth, json=json
        )


class StorefrontApi:
    lcu_api = LcuApi()
    token = lcu_api.request("GET", "/lol-login/v1/session").json()["idToken"]
    region = lcu_api.region

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(__class__, cls).__new__(cls)
        return cls.instance

    def request(self, method, endpoint, json=None):
        return requests.request(
            method,
            f"https://{self.region}.store.leagueoflegends.com{endpoint}",
            json=json,
            headers={"Authorization": f"Bearer {self.token}"},
        )
