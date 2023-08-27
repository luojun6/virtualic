import sys, inspect

from signals.enum_signals import EnumSignal
from signals.int_signals import SpeedSlider


def get_class_by_name(class_name: str) -> EnumSignal:
    return getattr(sys.modules[__name__], class_name)


def collect_classes() -> dict:
    all_signals = dict()
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            all_signals[name] = obj

    return all_signals


class VehSpdAvgDrvn(SpeedSlider):
    pass


class SysPwrMd(EnumSignal):
    OFF = 0
    ACC = 1
    RUN = 2
    CRANK = 3


class VehLckngSts(EnumSignal):
    Unlocked = 0
    Signal_Position_Entry_Unlocked = 1
    Interior_Locked = 2
    Exterior_Locked = 3
    Super_Locked = 4
    Reserved5 = 5
    Reserved6 = 6
    Unknow = 7
