# utils/apis.py

from os import path
import urllib3
from requests.auth import HTTPBasicAuth
import psutil
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_args_lockfile():
    LEAGUE_PATH = "C:\\Riot Games\\League of Legends"
    RIOT_CLIENT_PATH = path.expandvars("%LOCALAPPDATA%\\Riot Games\\Riot Client\\Config")

    process_args = {}

    with open(f"{LEAGUE_PATH}\\lockfile") as f:
        args = f.read().split(":")
        process_args.update({"app-port": args[2]})
        process_args.update({"remoting-auth-token": args[3]})

    with open(f"{RIOT_CLIENT_PATH}\\lockfile") as f:
        args = f.read().split(":")
        process_args.update({"riotclient-app-port": args[2]})
        process_args.update({"riotclient-auth-token": args[3]})

    return process_args


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
    port = process_args.get("app-port")
    auth = HTTPBasicAuth("riot", process_args.get("remoting-auth-token"))

    def __new__(cls):
        cls.region = cls.request(cls, "GET", "/riotclient/get_region_locale").json().get("webRegion")
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
    url = lcu_api.request("GET", "/lol-store/v1/getStoreUrl").json()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(__class__, cls).__new__(cls)
        return cls.instance

    def request(self, method, endpoint, json=None):
        return requests.request(
            method,
            f"{self.url}{endpoint}",
            json=json,
            headers={"Authorization": f"Bearer {self.token}"},
        )
