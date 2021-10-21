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

    def __init__(self, start_time, attack_time, start_amplitude, decay_time, sustain_amplitude, release_time):
        self.start_time = start_time
        self.attack_time = attack_time
        self.start_amplitude = start_amplitude
        self.decay_time = decay_time
        self.sustain_amplitude = sustain_amplitude
        self.release_time = release_time
        self.state = Attack(self, start_time)

    def set_state(self, state_id, *args):
        self.state = self.states[state_id](self, *args)

    def on_press(self, time):
        self.state.on_press(time)

    def on_release(self, time):
        self.state.on_release(time)

    def on_tick(self, time):
        self.state.on_tick(time)

    def get_amplitude(self, time):
        return self.state.get_amplitude(time)

    def is_finished(self):
        return self.state.is_finished()
