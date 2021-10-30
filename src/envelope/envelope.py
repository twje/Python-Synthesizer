from enum import Enum
from enum import auto
from .attack import Attack
from .decay import Decay
from .sustain import Sustain
from .release import Release


class Envelope:
    class STATE_ID(Enum):
        ATTACK = auto()
        DECAY = auto()
        SUSTAIN = auto()
        RELEASE = auto()

    states = {
        STATE_ID.ATTACK: Attack,
        STATE_ID.DECAY: Decay,
        STATE_ID.SUSTAIN: Sustain,
        STATE_ID.RELEASE: Release,
    }

    def __init__(self, attack_time, start_amplitude, decay_time, sustain_amplitude, release_time):
        self.attack_time = attack_time
        self.start_amplitude = start_amplitude
        self.decay_time = decay_time
        self.sustain_amplitude = sustain_amplitude
        self.release_time = release_time
        self.state = Attack(self, 0)

    def set_state(self, state_id, *args):
        self.state = self.states[state_id](self, *args)

    def copy(self):
        return Envelope(            
            self.attack_time,
            self.start_amplitude,
            self.decay_time,
            self.sustain_amplitude,
            self.release_time,
        )
