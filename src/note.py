

class Note:
    def __init__(self, index, instrument, start_time):
        self.index = index
        self.instrument = instrument
        self.envelope = self.instrument.envelope_factory(start_time)

    def play(self, time):
        life_time = time - self.envelope.start_time
        return self.instrument.sound(life_time, self.index) * self.amplitude(time)

    def amplitude(self, time):
        return self.envelope.get_amplitude(time)
