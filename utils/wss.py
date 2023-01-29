import json
import asyncio
import aiohttp

from collections import defaultdict
from apis import LcuApi, RiotClientApi
import apis


process_args = apis.process_args


class EventSubscription:
    async def _default_behavior(self, data):
        pass

    def __init__(self, default_behavior=None):
        self._registered_uris = {}
        self._registered_paths = {}

        if default_behavior:
            self._default_behavior = default_behavior

    def filter_endpoint(self, endpoint, handler=_default_behavior):
        if endpoint.endswith("/"):
            self._registered_paths[endpoint] = handler
        else:
            self._registered_uris[endpoint] = handler

    def unfilter_endpoint(self, endpoint):
        if endpoint.endswith("/"):
            del self._registered_paths[endpoint]
        else:
            del self._registered_uris[endpoint]

    def tasks(self, data):
        tasks = []

        for path_key, path_handler in self._registered_paths.items():
            if data["uri"].startswith(path_key):
                tasks.append(asyncio.create_task(path_handler(data)))

        uri_handler = self._registered_uris.get(data["uri"], None if tasks else self._default_behavior)
        if uri_handler:
            hasHandler = True
            tasks.append(asyncio.create_task(uri_handler(data)))

        return tasks


class LcuWebsocket:
    _port = process_args.get("app-port")
    _auth_token = process_args.get("remoting-auth-token")

    @classmethod
    async def start(cls):
        self = LcuWebsocket()
        self.ws_session = aiohttp.ClientSession(
            auth=aiohttp.BasicAuth("riot", self._auth_token), headers= {"Content-Type": "application/json", "Accept": "application/json"}
        )
        self.ws_client = await self.ws_session.ws_connect(f"wss://127.0.0.1:{self._port}", ssl=False)

        self.ws_subscriptions = defaultdict(list)
        self.subscription_tasks = []

        async def begin_ws_loop(self):
            async for msg in self.ws_client:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    if not msg.data:
                        pass
                    else:
                        data = json.loads(msg.data)

                        subscriptions = self.ws_subscriptions[data[1]]
                        for subscription in subscriptions:
                            self.subscription_tasks += subscription.tasks(data[2])

                            if self.subscription_tasks:
                                done, pending = await asyncio.wait(self.subscription_tasks, timeout=0)
                                for task in done:
                                    _ = await task
                                    self.subscription_tasks.remove(task)

                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    break

        self.ws_loop_task = asyncio.create_task(begin_ws_loop(self))
        return self

    async def close(self):
        await self.ws_client.close()
        await self.ws_session.close()
        await self.ws_loop_task
        await asyncio.gather(*self.subscription_tasks)

    async def subscribe(self, event, default_handler=None, subscription=None):
        if default_handler and subscription:
            pass

        if not self.ws_subscriptions[event]:
            await self.ws_client.send_json([5, event])

        if not subscription:
            subscription = EventSubscription(default_handler)

        self.ws_subscriptions[event].append(subscription)
        return subscription
        

class RiotClientWebsocket:
    _port = process_args.get("riotclient-app-port")
    _auth_token = process_args.get("riotclient-auth-token")

    @classmethod
    async def start(cls):
        self = RiotClientWebsocket()
        self.ws_session = aiohttp.ClientSession(
            auth=aiohttp.BasicAuth("riot", self._auth_token),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
        self.ws_client = await self.ws_session.ws_connect(f"wss://127.0.0.1:{self._port}", ssl=False)

        self.ws_subscriptions = defaultdict(list)
        self.subscription_tasks = []

        async def begin_ws_loop(self):
            async for msg in self.ws_client:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    if not msg.data:
                        pass
                    else:
                        data = json.loads(msg.data)

                        subscriptions = self.ws_subscriptions[data[1]]
                        for subscription in subscriptions:
                            self.subscription_tasks += subscription.tasks(data[2])

                            if self.subscription_tasks:
                                done, pending = await asyncio.wait(self.subscription_tasks, timeout=0)
                                for task in done:
                                    _ = await task
                                    self.subscription_tasks.remove(task)

                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    break

        self.ws_loop_task = asyncio.create_task(begin_ws_loop(self))
        return self

    async def close(self):
        await self.ws_client.close()
        await self.ws_session.close()
        await self.ws_loop_task
        await asyncio.gather(*self.subscription_tasks)

    async def subscribe(self, event, default_handler=None, subscription=None):
        if default_handler and subscription:
            pass

        if not self.ws_subscriptions[event]:
            await self.ws_client.send_json([5, event])

        if not subscription:
            subscription = EventSubscription(default_handler)

        self.ws_subscriptions[event].append(subscription)
        return subscription


async def start(win):
    global window
    window = win
    lcu_api = LcuApi()
    await gameflow_handler({"data": lcu_api.request("GET", "/lol-gameflow/v1/gameflow-phase").json()})
    riot_websocket = await RiotClientWebsocket.start()
    lcu_websocket = await LcuWebsocket.start()
    await lcu_websocket.subscribe("OnJsonApiEvent_lol-gameflow_v1_gameflow-phase", gameflow_handler)
    await lcu_websocket.subscribe("OnJsonApiEvent_lol-champions_v1_inventories", wallet_handler)
    (await riot_websocket.subscribe("OnJsonApiEvent_chat_v5_participants")).filter_endpoint(
        "/chat/v5/participants/champ-select", participants_handler
    )
    while True:
        await asyncio.sleep(100)

participants = []
cid = ""
async def participants_handler(data):
    global participants, cid
    if data.get("eventType") != "Update":
        return

    data = data.get("data")
    for e in data.get("participants"):
        if e.get("cid") != cid:
            participants = []
            cid = e.get("cid")
        participants.append(e.get("name"))
    window["-chat-"].update(participants)

async def gameflow_handler(data):
    data = data.get("data")
    match data:
        case "ChampSelect":
            window["-dodge-"].update(disabled=False)
            window["-boost-"].update(disabled=False)
        case _:
            window["-dodge-"].update(disabled=True)
            window["-boost-"].update(disabled=True)

async def wallet_handler(data):
    pass
