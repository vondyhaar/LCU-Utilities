import urllib3
from requests.auth import HTTPBasicAuth
from psutil import process_iter
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RiotClientApi:
    lcu_process = None

    def __init__(self) -> None:
        for e in process_iter():
            if e.name() == "LeagueClientUx.exe":
                 self.lcu_process = e
        
        self.get_auth()

    def request(self, method, endpoint):
        # proxies = {'https': ''}
        return requests.request(method=method, url=f"https://127.0.0.1:{self.port}{endpoint}", verify=False, auth=self.auth)

    def get_auth(self):
        process_args = {}
        for e in self.lcu_process.cmdline():
            if '=' in e:
                key, value = e[2:].split('=', 1)
                process_args.update({key: value})

        self.region = process_args.get("region")
        self.port = process_args.get("riotclient-app-port")
        self.auth = HTTPBasicAuth("riot", process_args.get("riotclient-auth-token"))


    


