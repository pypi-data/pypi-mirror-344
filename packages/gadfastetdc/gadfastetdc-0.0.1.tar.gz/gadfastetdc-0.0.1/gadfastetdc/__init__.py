import json
import typing

import etcd3
import fastapi


class Etcd:
    def __init__(self, url: str, storage: str, settings: typing.Any):
        host, port = url.split(":")
        self.client = etcd3.client(host=host, port=int(port))
        self.storage = storage
        self.settings = settings
        self.router = fastapi.APIRouter(tags=["Etcd"])
        self.endpoints()

    def get(self) -> dict[str, typing.Any]:
        config, _ = self.client.get(self.storage)
        return json.loads(config) if config else {}

    def set(self, config: dict[str, typing.Any]) -> None:
        self.client.put(self.storage, json.dumps(config))
        self.refresh()

    def refresh(self) -> None:
        config = self.get()
        for key, value in config.items():
            if hasattr(self.settings, key):
                setattr(self.settings, key, value)

    def endpoints(self) -> None:
        @self.router.get("/-/etcd")
        def get() -> dict:
            return self.get()

        @self.router.put("/-/etcd")
        def set(config: dict[str, typing.Any] = fastapi.Body(...)) -> None:
            self.set(config)


__all__ = ["Etcd"]
