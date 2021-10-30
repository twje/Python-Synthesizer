from util import to_hurtz


class Oscillation:
    def __init__(self, func, note_offset):
        self.func = func
        self.note_offset = note_offset


class Instrument:
    def __init__(self, name, volume, envelope):
        self.name = name
        self.volume = volume
        self.oscillations = []
        self.envelope = envelope

    def __call__(self, *args,  **kwds):
        return self

    def add_oscillation(self, osc, note_offset):
        self.oscillations.append(Oscillation(osc, note_offset))

    def sound(self, life_time, note_index):
        sound = 0
        for osc in self.oscillations:
            sound += osc.func(
                life_time,
                to_hurtz(note_index + osc.note_offset)
            )

        return self.volume * sound

    def envelope_factory(self):
        return self.envelope.copy()
