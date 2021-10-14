import math


class Note:
    def __init__(self, idz, envelope):
        self.idz = idz
        self.envelope = envelope

    def life_time(self, time):
        return time - self.envelope.start_time

    @staticmethod
    def to_hurtz(note_id):
        return 256 * math.pow(1.0594630943592952645618252949463, note_id)
