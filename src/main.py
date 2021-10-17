from queue import Queue
from audio_processor import AudioProcessor
from input_processor import InputProcessor
from visualizer import Visualizer
from audio import Audio
from piano import Piano

CHENNELS = 1
RATE = 44100
CHUNK = 1024

event_bus = Queue()

input_processor = InputProcessor(event_bus)
audio_processor = AudioProcessor(event_bus)
audio_processor.add_track(Piano())

input_processor.start()

visualizer = Visualizer(CHUNK, CHENNELS, scale=4)
audio = Audio(CHENNELS, RATE, CHUNK, audio_processor.on_tick)
with audio as stream:
    while stream.is_active():
        if not stream.empty():
            visualizer.update(stream.get())
