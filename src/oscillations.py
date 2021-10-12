import math
import random
from enum import Enum
from enum import auto


class OSC_TYPE(Enum):
    OSC_SINE = auto()
    OSC_SQUARE = auto()
    OSC_TRIANGLE = auto()
    OSC_SAW_ANA = auto()
    OSC_SAW_DIG = auto()
    OSC_NOISE = auto()


def hertz_to_angle(hertz):
    return hertz * 2 * math.pi


def osc(time, hertz, osc_type, LFOHertz=0, LFOAmplitude=0):
    if hertz == 0:
        return 0

    frequency = math.sin(hertz_to_angle(
        hertz)*time + LFOAmplitude * hertz * math.sin(hertz_to_angle(LFOHertz) * time))

    if osc_type == OSC_TYPE.OSC_SINE:
        return math.sin(frequency)
    elif osc_type == OSC_TYPE.OSC_SQUARE:
        signal = math.sin(frequency)
        if signal == 0:
            return 0
        elif signal > 0:
            return 1
        else:
            return - 1
    elif osc_type == OSC_TYPE.OSC_TRIANGLE:
        return math.asin(
            math.sin(frequency)
        ) * (2/math.pi)
    elif osc_type == OSC_TYPE.OSC_SAW_ANA:
        signal = 0
        for n in range(1, 40):
            signal += math.sin(n * frequency)/n
        return signal * (2/math.pi)
    elif osc_type == OSC_TYPE.OSC_SAW_DIG:
        return (2 / math.pi) * (hertz * math.pi * math.fmod(time, 1/hertz) - (math.pi / 2))
    elif osc_type == OSC_TYPE.OSC_NOISE:
        return random.uniform(-1, 1)

    return 0
