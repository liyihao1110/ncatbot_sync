from dataclasses import dataclass

@dataclass
class Status:
    """在线状态数据类"""
    status: int
    ext_status: int
    battery_status: int = 0

class StatusType:
    """预定义状态集合"""

    # 基础状态
    ONLINE = Status(10, 0)
    QME = Status(60, 0)
    AWAY = Status(30, 0)
    BUSY = Status(50, 0)
    DO_NOT_DISTURB = Status(70, 0)
    INVISIBLE = Status(40, 0)
    
    # 扩展状态
    LISTENING = Status(10, 1028)
    SPRING_FESTIVAL = Status(10, 2037)
    PLAYING_YUANMENG = Status(10, 2025)
    FIND_STAR_PARTNER = Status(10, 2026)
    EXHAUSTED = Status(10, 2014)
    WEATHER_TODAY = Status(10, 1030)
    CRASHED = Status(10, 2019)
    IN_LOVE = Status(10, 2006)
    LOVING = Status(10, 1051)
    GOOD_LUCK = Status(10, 1071)
    NO_MERCURY = Status(10, 1201)
    HAPPY_FLYING = Status(10, 1056)
    FULL_OF_ENERGY = Status(10, 1058)
    BABY_CERTIFIED = Status(10, 1070)
    COMPLICATED = Status(10, 1063)
    PLAYING_DUMB = Status(10, 2001)
    EMO = Status(10, 1401)
    TOO_HARD = Status(10, 1062)
    LET_IT_GO = Status(10, 2013)
    IM_FINE = Status(10, 1052)
    WANT_PEACE = Status(10, 1061)
    LEISURELY = Status(10, 1059)
    TRAVELING = Status(10, 2015)
    WEAK_SIGNAL = Status(10, 1011)
    GOING_OUT = Status(10, 2003)
    DOING_HOMEWORK = Status(10, 2012)
    STUDYING = Status(10, 1018)
    WORKING = Status(10, 2023)
    SLACKING = Status(10, 1300)
    BORED = Status(10, 1060)
    PLAYING_GAME = Status(10, 1027)
    SLEEPING = Status(10, 1016)
    NIGHT_OWL = Status(10, 1032)
    WATCHING_DRAMA = Status(10, 1021)
    VERY_COLD = Status(10, 2050)
    JANUARY_HELLO = Status(10, 2053)
    
    # 特殊状态（需动态设置电池值）
    BATTERY = Status(10, 1000)
