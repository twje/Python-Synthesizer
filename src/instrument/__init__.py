import json
import os
from .instrument import Instrument
from .oscilations import oscilations
from envelope import Envelope


def load_oscillations(sound):
    for osc_def in sound:
        osc_closure = oscilations[osc_def["osc"]]
        osc_func = osc_closure(
            osc_def["scale"],
            osc_def["lfo_hertz"],
            osc_def["lfo_amplitude"]
        )
        yield osc_func, osc_def["note_offset"]


def load_instruments(filepath):
    instruments = {}

    with open(filepath) as fp:
        data = json.load(fp)

    for instrument_def in data:
        name = instrument_def["name"]
        instrument = Instrument(
            name,
            instrument_def["volume"],
            Envelope(**instrument_def["envelope"]),
        )

        for osc in load_oscillations(instrument_def["sound"]):
            instrument.add_oscillation(*osc)

        instruments[name] = instrument

    return instruments
