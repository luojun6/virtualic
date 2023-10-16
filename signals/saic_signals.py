import sys, inspect

from signals.enum_signals import EnumSignal
import signals.int_signals as IntSliderSignals


def get_class_by_name(class_name: str) -> EnumSignal:
    return getattr(sys.modules[__name__], class_name)


def collect_classes() -> dict:
    all_signals = dict()
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            all_signals[name] = obj

    return all_signals


class VehSpdAvgDrvn(IntSliderSignals.SpeedSlider):
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
    
class TrShftLvrPos(EnumSignal):
    BetweenRanges = 0
    ParkRange = 1
    ReverseRange = 2
    NeutralRange = 3
    ForwardRangeA = 4
    ForwardRangeB = 5
    ForwardRangeC = 6
    ForwardRangeD = 7
    ForwardRangeE = 8
    ForwardRangeF = 9
    ForwardRangeG = 10
    ForwardRangeH = 11
    LeverPositionUnknown = 15
    
    @classmethod
    def _missing_(cls, value):
        return cls.ParkRange
    
class DircnIndLampSwSts(EnumSignal):
    off = 0
    Left_On = 1
    Right_On = 2
    reverse = 3
    
class LDircnIO(EnumSignal):
    OFF = 0
    ON = 1
    
class RDircnIO(EnumSignal):
    OFF = 0
    ON = 1
    
class StrgWhlAng(IntSliderSignals.SteeringWheelAngle):
    pass


class VehDrvngMd(EnumSignal):
    NoDrivingMode = 0
    SuperEco = 1
    ECO = 2
    Normal = 3
    Sport = 4
    SuperSport = 5
    Snow = 6
    CustomizationMode = 7