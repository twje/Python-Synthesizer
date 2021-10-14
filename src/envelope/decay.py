
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

    def on_tick(self, time):
        life_time = time - self.start_time
        if life_time >= self.envelope.decay_time:
            self.envelope.set_state(
                self.envelope.STATE_ID.SUSTAIN,
                time,
                self.is_released
            )

    def get_amplitude(self, time):
        life_time = time - self.start_time
        return (life_time / self.envelope.decay_time) * (self.envelope.sustain_amplitude - self.envelope.start_amplitude) + self.envelope.start_amplitude

    def is_finished(self):
        return False
