from apis import *
from psutil import process_iter
import time
import shutil


lcu_api = LcuApi()


def remove_tokens():
    data = {"challengeIds": [-1, -1, -1]}
    r = lcu_api.request("post", "/lol-challenges/v1/update-player-preferences", data)


def change_background(id):
    data = {"key": "backgroundSkinId", "value": id}
    r = lcu_api.request("post", "/lol-summoner/v1/current-summoner/summoner-profile", data)


def cleaner():
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
        "C:\\ProgramData\\Riot Games\\machine.cfg",
        "C:\\Riot Games\\League of Legends\\debug.log",
        "C:\\Riot Games\\Riot Client\\UX\\natives_blob.bin",
        "C:\\Riot Games\\Riot Client\\UX\\snapshot_blob.bin",
        "C:\\Riot Games\\Riot Client\\UX\\v8_context_snapshot.bin",
        "C:\\Riot Games\\Riot Client\\UX\\icudtl.dat",
    ]
    dir_list = [
        "C:\\ProgramData\\Riot Games",
        "C:\\Riot Games\\League of Legends\\Config",
        "C:\\Riot Games\\League of Legends\\Logs",
    ]
