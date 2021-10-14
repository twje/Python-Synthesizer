class Sustain:
    def __init__(self, envelope, start_time, is_released):
        print("sustain")
        self.envelope = envelope
        self.start_time = start_time
        self.is_released = is_released

    def on_press(self, time):
        pass

    def on_release(self, time):
        if self.envelope.sustain_amplitude > 0:
            self.set_release_state(time)

    def on_tick(self, time):
        if self.envelope.sustain_amplitude > 0 and self.is_released:
            self.set_release_state(time)
        elif self.envelope.sustain_amplitude == 0:
            self.envelope.set_state(self.envelope.STATE_ID.IDLE)

    def get_amplitude(self, time):
        return self.envelope.sustain_amplitude

    def is_finished(self):
        return False

    def set_release_state(self, time):
        self.envelope.set_state(self.envelope.STATE_ID.RELEASE, time)
