
from player import Player
from input_processor import InputProcessor
from visualizer import Visualizer
from audio import Audio
from piano import Piano

CHENNELS = 1
RATE = 44100
CHUNK = 1024

input_processor = InputProcessor()
player = Player(input_processor.event_bus)
player.add_track(Piano())

input_processor.start()

visualizer = Visualizer(CHUNK, CHENNELS, scale=4)
audio = Audio(CHENNELS, RATE, CHUNK, player)
with audio as stream:
    while stream.is_active():
        if not stream.empty():
            visualizer.update(stream.get())

audio.stop()
