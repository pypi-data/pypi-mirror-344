import enum
from typing import List, Optional


ESP32: USBDeviceType = USBDeviceType.ESP32

FTDI: USBDeviceType = USBDeviceType.FTDI

class FreeWiliDevice:
    def __init__(self) -> None: ...

    def __str__(self) -> str: ...

    @property
    def name(self) -> str: ...

    @property
    def serial(self) -> str: ...

    @property
    def usb_hub(self) -> USBDevice: ...

    @property
    def usb_devices(self) -> List[USBDevice]: ...

    def get_usb_devices(self, arg: USBDeviceType, /) -> List[USBDevice]: ...

Hub: USBDeviceType = USBDeviceType.Hub

MassStorage: USBDeviceType = USBDeviceType.MassStorage

Other: USBDeviceType = USBDeviceType.Other

Serial: USBDeviceType = USBDeviceType.Serial

SerialDisplay: USBDeviceType = USBDeviceType.SerialDisplay

SerialMain: USBDeviceType = USBDeviceType.SerialMain

class USBDevice:
    def __init__(self) -> None: ...

    def __str__(self) -> str: ...

    @property
    def kind(self) -> USBDeviceType: ...

    @property
    def vid(self) -> int: ...

    @property
    def pid(self) -> int: ...

    @property
    def name(self) -> str: ...

    @property
    def serial(self) -> str: ...

    @property
    def location(self) -> int: ...

    @property
    def paths(self) -> Optional[List[str]]: ...

    @property
    def port(self) -> Optional[str]: ...

class USBDeviceType(enum.Enum):
    Hub = 0

    Serial = 1

    SerialMain = 2

    SerialDisplay = 3

    MassStorage = 4

    ESP32 = 5

    FTDI = 6

    Other = 7

def find_all() -> List[FreeWiliDevice]: ...
