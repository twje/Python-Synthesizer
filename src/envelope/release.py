class Release:
    def __init__(self, envelope, start_time):
        print("release")
        self.envelope = envelope
        self.start_time = start_time
        self.finished = False

    def on_press(self, life_time):
        elapsed_time = life_time - self.start_time
        if elapsed_time < self.envelope.release_time:
            attack_gradient = self.envelope.start_amplitude / self.envelope.attack_time
            offset = self.get_amplitude(life_time) / attack_gradient
            self.envelope.set_state(
                self.envelope.STATE_ID.ATTACK,
                life_time - offset
            )

    def on_release(self, time):
        pass

    def on_tick(self, life_time):
        elapsed_time = life_time - self.start_time
        self.finished = elapsed_time >= self.envelope.release_time

    def get_amplitude(self, life_time):
        elapsed_time = life_time - self.start_time
        return self.envelope.sustain_amplitude - elapsed_time * self.envelope.sustain_amplitude/self.envelope.release_time

    def is_finished(self):
        return self.finished
