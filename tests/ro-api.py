
# import rblxopencloud
import orjson
import aiohttp
import asyncio

from typing import Union, Optional

token = "MS8Vu1W5GUq60aOXZ+7ZIMMXqsh9QDSdNaTHK1jAEdDlO+k/"
universeId = 4284784630


class DataStore:
    def __init__(self,
                 universeId: Union[str, int],
                 datastore: str,
                 api_key: str,
                 _session: Optional[aiohttp.ClientSession] = None):
        self.universeId = universeId
        self.datastore = datastore
        self.api_key = api_key

        if _session is None:
            _session = aiohttp.ClientSession()
        self._session = _session

        self.base_url = "https://apis.roblox.com/datastores/v1/universes"
        self._list_objects_url = (f"{self.base_url}/{universeId}/"
                                  "standard-datastores/datastore/entries")
        self._objects_url = f"{self._list_objects_url}/entry"
        self._increment_url = f"{self._objects_url}/increment"
        self._version_url = f"{self._objects_url}/versions/version"

    async def __aenter__(self):
        return self

    async def __aexit__(self,
                        universeId: Union[str, int],
                        datastore: str, api_key: str,
                        _session: Optional[aiohttp.ClientSession] = None):
        await self._session.close()

    def sesseion_requsts(self, method: str, url: str, **kwargs):
        return self._session.request(method=method, url=url, **kwargs)

    async def keys(self, prefix: str = "", limit: int = None) -> list:
        ret = []
        nextcursor = ""
        while limit is None or len(ret) < limit:
            headers = {"x-api-key": token}
            params = {
                "datastoreName": self.datastore,
                "prefix": prefix,
                "cursor": nextcursor
            }
            response = await self.sesseion_requsts(
                "GET",
                self._list_objects_url,
                headers=headers,
                params=params
            )
            data = await response.json()
            if 'keys' not in data:
                break
            for key in data["keys"]:
                yield key["key"]
                ret.append(key["key"])
            nextcursor = data.get("nextPageCursor")
            if not nextcursor:
                break

    async def get(self, key):
        headers = {
            'x-api-key': token
        }
        params = {
            "datastoreName": self.datastore,
            "entryKey": key
        }

        responce = await self.sesseion_requsts(
            "GET",
            self._objects_url,
            headers=headers,
            params=params
        )

        content = await responce.read()
        return content

    async def set(self, key, value):
        headers = {
            'x-api-key': token
        }
        params = {
            "datastoreName": self.datastore,
            "entryKey": key
        }
        data = orjson.dumps(value).decode()

        responce = await self.sesseion_requsts(
            "POST",
            self._objects_url,
            data=data,
            headers=headers,
            params=params
        )

        json = await responce.json()
        return json

    async def increment(self, key: str, increment: Union[int, float]):
        headers = {
            "x-api-key": self.api_key
        }
        params = {
            "datastoreName": self.datastore,
            "entryKey": key,
            "incrementBy": increment
        }

        response = await self.sesseion_requsts(
            "POST",
            self._increment_url,
            headers=headers,
            params=params
        )

        content = await response.read()
        return content

    async def delete(self, key):
        headers = {
            'x-api-key': token
        }
        params = {
            "datastoreName": self.datastore,
            "entryKey": key
        }

        await self.sesseion_requsts(
            "DELETE",
            self._objects_url,
            headers=headers,
            params=params
        )


async def main():
    async with DataStore(universeId, "BanDS", token) as db:
        async for key in db.keys(limit=10):
            print(key)


# expr = rblxopencloud.Experience(universeId, api_key=token)
asyncio.run(main())
