import math

oscilations = {}


def register_oscilation(name):
    def add_to_regsitry(func):
        oscilations[name] = func
        return func
    return add_to_regsitry


def hertz_to_angle(hertz):
    return hertz * 2 * math.pi


def modulate(time, hertz, lfoHertz, lfoAmplitude):
    return math.sin(hertz_to_angle(hertz) * time + lfoAmplitude * hertz * math.sin(hertz_to_angle(lfoHertz) * time))


@register_oscilation("sine")
def sine(scale, lfoHertz, lfoAmplitude):
    # wrap
    def sound(time, hertz):
        return scale * math.sin(modulate(time, hertz, lfoHertz, lfoAmplitude))
    return sound
