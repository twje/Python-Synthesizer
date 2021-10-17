from envelope import Envelope
from oscillations import osc
from oscillations import OSC_TYPE
from note import Note


class Bell:
    def __init__(self):
        self.volume = 1

    def sound(self, life_time, note_id):
        #life_time = note.life_time(time)
        sound = (
            + 1 * osc(life_time, Note.to_hurtz(note_id + 12),
                      OSC_TYPE.OSC_SINE, 5, 0.001)
            + 0.5 * osc(life_time, Note.to_hurtz(note_id + 24),
                        OSC_TYPE.OSC_SINE)
            + 0.25 + osc(life_time, Note.to_hurtz(note_id + 36),
                         OSC_TYPE.OSC_SINE)
        )
        return self.volume * sound

    def envelope_factory(self, time):
        return Envelope(
            time,
            attack_time=0.01,
            start_amplitude=1,
            decay_time=0.01,
            sustain_amplitude=0.3,
            release_time=0.1
        )
