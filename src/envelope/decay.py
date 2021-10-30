
class Decay:
    def __init__(self, envelope, start_time, is_released):
        print("decay")
        self.envelope = envelope
        self.start_time = start_time
        self.is_released = is_released

    def on_press(self, time):
        self.is_released = False

    def on_release(self, time):
        self.is_released = True

    def on_tick(self, life_time):
        elapsed_time = life_time - self.start_time
        if elapsed_time >= self.envelope.decay_time:
            self.envelope.set_state(
                self.envelope.STATE_ID.SUSTAIN,
                self.is_released
            )

    def get_amplitude(self, life_time):
        elapsed_time = life_time - self.start_time
        return self.envelope.start_amplitude + (elapsed_time / self.envelope.decay_time) * (self.envelope.sustain_amplitude - self.envelope.start_amplitude)

    def is_finished(self):
        return False
