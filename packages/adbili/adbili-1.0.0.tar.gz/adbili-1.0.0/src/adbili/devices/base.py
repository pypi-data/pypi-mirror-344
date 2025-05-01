from abc import ABC, abstractmethod
from contextlib import contextmanager


class IDevice(ABC):
    @classmethod
    def create(cls, host: str, port: int) -> "IDevice":
        return cls(host, port)

    @abstractmethod
    def run(self, cmd: str) -> str:
        pass

    @abstractmethod
    def close(self) -> None:
        pass


DEVICES: dict[str, IDevice] = {}
DEFAULT_DEVICE: list[str] = []


def register_device(name: str, default: bool = False):
    def wrapper(cls):
        DEVICES[name] = cls
        if default:
            if len(DEFAULT_DEVICE) == 0:
                DEFAULT_DEVICE.append(name)
            else:
                print(
                    f"[Warning] default device changed: {DEFAULT_DEVICE[0]} -> {name}"
                )
                DEFAULT_DEVICE[0] = name
        elif len(DEFAULT_DEVICE) == 0:
            DEFAULT_DEVICE.append(name)
        return cls

    return wrapper


@contextmanager
def open(host: str, port: int):
    try:
        device = DEVICES[DEFAULT_DEVICE[0]].create(host, port)
        yield device
    finally:
        device.close()
