from functools import wraps
import random
import math

oscilations = {}


def register_oscilation(name):
    def add_to_regsitry(func):
        oscilations[name] = func
        return func
    return add_to_regsitry


def hertz_to_angle(hertz):
    return hertz * 2 * math.pi


def modulate(time, hertz, lfo_hertz, lfo_amplitude):
    return math.sin(hertz_to_angle(hertz) * time + lfo_amplitude * hertz * math.sin(hertz_to_angle(lfo_hertz) * time))


@register_oscilation("sine")
def sine(scale, lfo_hertz, lfo_amplitude):
    @wraps(sine)
    def sound(time, hertz):
        return scale * math.sin(modulate(time, hertz, lfo_hertz, lfo_amplitude))
    return sound


@register_oscilation("square")
def square(scale, lfo_hertz, lfo_amplitude):
    @wraps(square)
    def sound(time, hertz):
        signal = scale * \
            math.sin(modulate(time, hertz, lfo_hertz, lfo_amplitude))
        if signal == 0:
            return 0
        elif signal > 0:
            return 1
        else:
            return - 1
    return sound


@register_oscilation("triangle")
def triangle(scale, lfo_hertz, lfo_amplitude):
    @wraps(triangle)
    def sound(time, hertz):
        return math.asin(math.sin(modulate(time, hertz, lfo_hertz, lfo_amplitude))) * (2/math.pi)
    return sound


@register_oscilation("saw_ana")
def saw_ana(scale, lfo_hertz, lfo_amplitude):
    @wraps(saw_ana)
    def sound(time, hertz):
        signal = 0
        frequency = modulate(time, hertz, lfo_hertz, lfo_amplitude)
        for n in range(1, 100):
            signal += math.sin(n * frequency)/n
        return signal * (2/math.pi)
    return sound


@register_oscilation("saw_dig")
def saw_dig(scale, lfo_hertz, lfo_amplitude):
    @wraps(saw_dig)
    def sound(time, hertz):
        return (2 / math.pi) * (hertz * math.pi * math.fmod(time, 1/hertz) - (math.pi / 2))
    return sound


@register_oscilation("noise")
def noise(scale, lfo_hertz, lfo_amplitude):
    @wraps(noise)
    def sound(time, hertz):
        return random.uniform(-1, 1)
    return sound
