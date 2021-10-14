from factory import create_audio_processor
from visualizer import Visualizer
from piano import Piano

CHENNELS = 1
RATE = 44100
CHUNK = 1024


audio_processor = create_audio_processor()
audio_processor.add_track(Piano())

visualizer = Visualizer(CHUNK, CHENNELS, scale=4)
with audio_processor.start(CHENNELS, RATE, CHUNK) as stream:
    while stream.is_active():
        if not stream.empty():
            visualizer.update(stream.get())
