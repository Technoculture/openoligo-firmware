"""
Provides the platform on which the program is running.
"""
from enum import Enum


def is_rpi() -> bool:
    """Returns True if running on a Raspberry Pi, False otherwise."""
    try:
        with open("/proc/cpuinfo", "r", encoding="utf-8") as file:
            return "Raspberry" in file.read()
    except FileNotFoundError:
        return False


def is_bb() -> bool:
    """Returns True if running on a Raspberry Pi, False otherwise."""
    try:
        with open("/proc/cpuinfo", "r", encoding="utf-8") as file:
            return "AM33XX" in file.read()
    except FileNotFoundError:
        return False


class Platform(Enum):
    """Platform type."""

    RPI = "RPI"
    BB = "BB"
    SIM = "SIM"


def get_platform() -> Platform:
    """Get the platform type."""
    if is_rpi():
        return Platform.RPI
    if is_bb():
        return Platform.BB
    return Platform.SIM


__platform__ = get_platform()


MinimumCommonPinout = dict[str, str]


rpi_board_pins: MinimumCommonPinout = {
    "P3": "3",
    "P5": "5",
    "P7": "7",
    "P8": "8",
    "P10": "10",
    "P11": "11",
    "P12": "12",
    "P13": "13",
    "P15": "15",
    "P16": "16",
    "P18": "18",
    "P19": "19",
    "P21": "21",
    "P22": "22",
    "P23": "23",
    "P24": "24",
    "P26": "26",
    "P27": "27",
    "P28": "28",
    "P29": "29",
    "P31": "31",
    "P32": "32",
    "P33": "33",
    "P35": "35",
    "P36": "36",
    "P37": "37",
    "P38": "38",
    "P40": "40",
}


bb_board_pins: MinimumCommonPinout = {
    "P3": "P8_3",
    "P5": "P8_4",
    "P7": "P8_5",
    "P8": "P8_6",
    "P10": "P8_7",
    "P11": "P8_8",
    "P12": "P8_9",
    "P13": "P8_10",
    "P15": "P8_11",
    "P16": "P8_12",
    "P18": "P8_13",
    "P19": "P8_14",
    "P21": "P8_15",
    "P22": "P8_16",
    "P23": "P8_17",
    "P24": "P8_18",
    "P26": "P8_19",
    "P27": "P8_20",
    "P28": "P8_21",
    "P29": "P8_22",
    "P31": "P9_11",
    "P32": "P8_24",
    "P33": "P8_25",
    "P35": "P8_26",
    "P36": "P8_27",
    "P37": "P8_28",
    "P38": "P8_29",
    "P40": "P8_30",
    "P41": "P8_31",
    "P42": "P8_32",
    "P43": "P8_33",
    "P44": "P8_34",
    "P45": "P8_35",
    "P46": "P8_36",
    "P47": "P8_37",
    "P48": "P8_38",
    "P49": "P8_39",
    "P50": "P8_40",
    "P51": "P8_41",
    "P52": "P8_42",
    "P53": "P8_43",
    "P54": "P8_44",
    "P55": "P8_45",
    "P56": "P8_46",
    "P57": "P9_12",
}


PLATFORM_TO_BOARD: dict[Platform, MinimumCommonPinout] = {
    Platform.BB: bb_board_pins,
    Platform.RPI: rpi_board_pins,
    Platform.SIM: rpi_board_pins,
}
