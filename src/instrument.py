from envelope import Envelope
from oscillations import osc
from oscillations import OSC_TYPE
from note import Note


class Instrument:
    def __init__(self):
        self.volume = 0
        self.envelopes = {}

    def sound(self, note, time):
        note.instruments.add(self)
        envelope = self.get_envelope(note, time)
        return self.sound_hook(time, note, envelope)

    def on_press(self, note, time):
        envelope = self.get_envelope(note, time)
        envelope.on_press(time)

    def on_release(self, note, time):
        envelope = self.get_envelope(note, time)
        envelope.on_release(time)

    def is_finished(self, note):
        return self.envelopes[note].is_finished()

    def get_envelope(self, note, time):
        if note not in self.envelopes:
            self.envelopes[note] = self.envelope_factory(time)
        return self.envelopes[note]

    def remove_envelope(self, note):
        del self.envelopes[note]

    # -----
    # Hooks
    # -----
    def sound_hook(self, time, note, envelope):
        pass

    def envelope_factory(self, note):
        pass


class Bell(Instrument):
    def __init__(self):
        super().__init__()
        self.volume = 1

    def sound_hook(self, time, note, envelope):        
        envelope.on_tick(time)
        amplitude = envelope.get_amplitude(time)
        life_time = time - envelope.start_time

        sound = (
            + 1 * osc(life_time, Note.to_hurtz(note.idz + 12),
                      OSC_TYPE.OSC_SINE, 5, 0.001)
            + 0.5 * osc(life_time, Note.to_hurtz(note.idz + 24),
                        OSC_TYPE.OSC_SINE)
            + 0.25 + osc(life_time, Note.to_hurtz(note.idz + 36),
                         OSC_TYPE.OSC_SINE)
        )
        return self.volume * amplitude * sound

    def envelope_factory(self, time):
        print(len(self.envelopes) + 1)
        return Envelope(
            time,
            attack_time=0.01,
            start_amplitude=1,
            decay_time=0.1,
            sustain_amplitude=0.3,
            release_time=1
        )
