import math


class Note:
    def __init__(self, idz):
        self.idz = idz
        self.instruments = set()

    def is_finished(self):
        return all(instrument.is_finished(self) for instrument in self.instruments)

    def destroy(self):
        for instrument in self.instruments:
            instrument.remove_envelope(self)

    def on_press(self, time):
        for instrument in self.instruments:
            instrument.on_press(self, time)

    def on_release(self, time):
        for instrument in self.instruments:
            instrument.on_release(self, time)

    @staticmethod
    def to_hurtz(note_id):
        return 256 * math.pow(1.0594630943592952645618252949463, note_id)
