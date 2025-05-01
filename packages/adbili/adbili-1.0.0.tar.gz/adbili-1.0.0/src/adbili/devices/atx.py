try:
    import adbutils
except ImportError:
    print("pip install adbutils")
    raise

from adbili.devices import IDevice, register_device

# @DeprecationWarning("Use AdbCliDevice instead")
@register_device("atx")
class AtxDevice(IDevice):
    """
    AdbDevice from openatx/adbutils
    """

    def __init__(self, host: str, port: int):
        self.addr = f"{host}:{port}"
        self.adb = adbutils.AdbClient(host=host, port=port)
        self.device = self.adb.device()

    def run(self, cmd: str) -> str:
        return self.device.shell(cmd)

    def close(self) -> None:
        self.adb.disconnect(self.addr)
