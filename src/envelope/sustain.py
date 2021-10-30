class Sustain:
    def __init__(self, envelope, is_released):
        print("sustain")
        self.envelope = envelope
        self.is_released = is_released

    def on_press(self, life_time):
        pass

    def on_release(self, life_time):
        if self.envelope.sustain_amplitude > 0:
            self.set_release_state(life_time)

    def on_tick(self, time):
        if self.envelope.sustain_amplitude > 0 and self.is_released:
            self.set_release_state(time)

    def get_amplitude(self, time):
        return self.envelope.sustain_amplitude

    def is_finished(self):
        return self.envelope.sustain_amplitude == 0

    def set_release_state(self, time):
        self.envelope.set_state(self.envelope.STATE_ID.RELEASE, time)
