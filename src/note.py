class Note:
    def __init__(self, index, instrument, start_time):
        self.index = index
        self.start_time = start_time
        self.instrument = instrument
        self.envelope = self.instrument.envelope_factory()
        self.ttl = 0

    def play(self, time):
        life_time = time - self.start_time
        if self.is_ready_to_expire(life_time):
            self.expire(life_time)

        return self.generate_sound(life_time)

    def generate_sound(self, life_time):
        return self.instrument.sound(life_time, self.index) * self.envelope.get_amplitude(life_time)

    def on_press(self, time):
        life_time = time - self.start_time
        self.envelope.on_press(life_time)

    def on_release(self, time):
        if self.ttl == 0:
            life_time = time - self.start_time
            self.envelope.on_release(life_time)

    def on_tick(self, time):
        life_time = time - self.start_time
        self.envelope.on_tick(life_time)

    def is_finished(self):
        return self.envelope.is_finished()

    def is_ready_to_expire(self, life_time):
        return self.ttl > 0 and life_time >= self.ttl

    def expire(self, life_time):
        print("HERE")
        self.envelope.on_release(life_time)
        self.ttl = 0
