class Idle:
    def __init__(self, envelope):
        print("idle")   
        self.envelope = envelope
        self.finished = False

    def on_press(self, time):
        pass

    def on_release(self, time):
        self.finished = True

    def on_tick(self, time):
        pass

    def get_amplitude(self, time):
        return 0

    def is_finished(self):
        return self.finished
