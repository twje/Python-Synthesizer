class Release:
    def __init__(self, envelope, start_time):
        print("release")   
        self.envelope = envelope
        self.start_time = start_time
        self.finished = False

    def on_press(self, time):
        life_time = time - self.start_time
        if life_time < self.envelope.release_time:
            attack_gradient = self.envelope.start_amplitude / self.envelope.attack_time
            offset = self.get_amplitude(time) / attack_gradient
        else:
            offset = 0
        self.envelope.set_state(self.envelope.STATE_ID.ATTACK, time - offset)

    def on_release(self, time):
        pass

    def on_tick(self, time):        
        life_time = time - self.start_time
        self.finished = life_time >= self.envelope.release_time

    def get_amplitude(self, time):
        life_time = time - self.start_time
        return self.envelope.sustain_amplitude - life_time * self.envelope.sustain_amplitude/self.envelope.release_time

    def is_finished(self):
        return self.finished
