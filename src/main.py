
from visualizer_plugin import VisualizerPlugin
from input_processor import InputProcessor
from player import Player
from audio import Audio
from piano import Piano
from instrument import load_instruments

CHENNELS = 1
RATE = 44100
CHUNK = 1024

instruments = load_instruments("..\def.json")

input_processor = InputProcessor()
input_processor.start()

player = Player(input_processor.event_bus)
player.add_track(Piano(instruments["bell"]))

audio = Audio(CHENNELS, RATE, CHUNK, player)
audio.plugins.append(VisualizerPlugin(CHUNK, CHENNELS, 4))

with audio as stream:
    while stream.is_active():
        stream.update_plugins()

audio.stop()
