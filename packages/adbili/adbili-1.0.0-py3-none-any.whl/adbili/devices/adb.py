import subprocess
import os

from adbili.devices import IDevice, register_device


@register_device("adb", default=True)
class AdbCliDevice(IDevice):
    """
    delegate to adb cli
    """

    def __init__(self, host: str, port: int):
        pass

    def run(self, cmd: str) -> str:
        result = subprocess.run(f"adb shell '{cmd}'", shell=True, capture_output=True)
        if result.stderr:
            print(result.stderr.decode("utf-8"))
        return result.stdout.decode("utf-8")
        # return os.system(f"adb shell '{cmd}'")

    def close(self) -> None:
        pass
