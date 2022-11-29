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


class RiotClientApi:
    def __init__(self) -> None:
        process_args = get_args()
        self.region = process_args.get("region")
        self.port = process_args.get("riotclient-app-port")
        self.auth = HTTPBasicAuth("riot", process_args.get("riotclient-auth-token"))

    def request(self, method, endpoint):
        return requests.request(
            method=method, url=f"https://127.0.0.1:{self.port}{endpoint}", verify=False, auth=self.auth
        )


class LcuApi:
    def __init__(self) -> None:
        process_args = get_args()
        self.region = process_args.get("region")
        self.port = process_args.get("app-port")
        self.auth = HTTPBasicAuth("riot", process_args.get("remoting-auth-token"))

    def request(self, method, endpoint):
        return requests.request(
            method=method, url=f"https://127.0.0.1:{self.port}{endpoint}", verify=False, auth=self.auth
        )
