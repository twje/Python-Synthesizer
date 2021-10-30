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

    def on_tick(self, life_time):
        elapsed_time = life_time - self.start_time        
        if elapsed_time >= self.envelope.attack_time:
            self.envelope.set_state(
                self.envelope.STATE_ID.DECAY,
                life_time,
                self.is_released
            )

    def get_amplitude(self, life_time):
        elapsed_time = life_time - self.start_time
        return (elapsed_time / self.envelope.attack_time) * self.envelope.start_amplitude

    def is_finished(self):
        return False
