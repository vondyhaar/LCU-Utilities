import os
from os import path
from apis import *
from psutil import process_iter
import time
import shutil


lcu_api = LcuApi()

def invis_banner():
    r = lcu_api.request("POST", "/lol-challenges/v1/update-player-preferences/", {"bannerAccent": "2"})
    print(r.status_code)

def restore_ux() -> None | str:
    r = lcu_api.request("POST", "/riotclient/launch-ux")
    if r.status_code != 204:
        return "Error"


def kill_ux() -> None | str:
    r = lcu_api.request("POST", "/riotclient/kill-ux")
    if r.status_code != 204:
        return "Error"


def remove_tokens() -> None:
    data = {"challengeIds": []}
    r = lcu_api.request("POST", "/lol-challenges/v1/update-player-preferences", data)


def change_background(id) -> None:
    data = {"key": "backgroundSkinId", "value": id}
    r = lcu_api.request("POST", "/lol-summoner/v1/current-summoner/summoner-profile", data)


def cleaner():  # https://github.com/notfeels/lol_cleaner
    process_list = [
        "LeagueCrashHandler.exe",
        "LeagueClientUx.exe",
        "League of Legends.exe",
        "LeagueClient.exe",
        "RiotClientServices.exe",
    ]
    for e in process_iter():
        if e.name() in process_list:
            e.kill()
    time.sleep(3)
    file_list = [
        "C:\\Riot Games\\League of Legends\\debug.log",
    ]
    dir_list = [
        "C:\\ProgramData\\Riot Games",
        "C:\\Riot Games\\League of Legends\\Config",
        "C:\\Riot Games\\League of Legends\\Logs",
        path.expandvars("%LOCALAPPDATA%\\Riot Games"),
    ]
    for e in file_list:
        try:
            os.remove(e)
            print(f"Removed {e} file")
        except OSError:
            os.chmod(e, 128)
            os.remove(e)
    for e in dir_list:
        if os.path.isdir(e):
            shutil.rmtree(e, ignore_errors=True)
            print(f"Removed {e} folder")


def change_rank(rank, queue, division="V"):
    data = {
        "lol": {
            "rankedLeagueDivision": f"{division}",
            "rankedLeagueQueue": f"{queue}",
            "rankedLeagueTier": f"{rank}",
        }
    }
    r = lcu_api.request("PUT", "/lol-chat/v1/me", data)
    print(r.json())
