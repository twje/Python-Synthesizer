class Attack:
    def __init__(self, envelope, start_time):
        print("attack")
        self.envelope = envelope
        self.start_time = start_time
        self.is_released = False

    def on_press(self, time):
        self.is_released = False

    def on_release(self, time):
        self.is_released = True

    def on_tick(self, time):
        life_time = time - self.start_time
        if life_time >= self.envelope.attack_time:
            self.envelope.set_state(
                self.envelope.STATE_ID.DECAY,
                self.start_time + self.envelope.attack_time,
                self.is_released
            )

    def get_amplitude(self, time):
        life_time = time - self.start_time
        return (life_time / self.envelope.attack_time) * self.envelope.start_amplitude

    def is_finished(self):
        return False
