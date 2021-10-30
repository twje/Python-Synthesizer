class Note:
    def __init__(self, index, instrument, start_time):
        self.index = index
        self.start_time = start_time
        self.instrument = instrument
        self.envelope = self.instrument.envelope_factory()

    @property
    def state(self):
        return self.envelope.state

    def play(self, time):
        life_time = time - self.start_time
        return self.instrument.sound(life_time, self.index) * self.amplitude(time)

    def amplitude(self, time):
        life_time = time - self.start_time
        return self.state.get_amplitude(life_time)

    def on_press(self, time):
        life_time = time - self.start_time
        self.state.on_press(life_time)

    def on_release(self, time):
        life_time = time - self.start_time
        self.state.on_release(life_time)

    def on_tick(self, time):
        life_time = time - self.start_time
        self.state.on_tick(life_time)

    def is_finished(self):
        return self.state.is_finished()
