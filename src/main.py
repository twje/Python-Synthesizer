
from audio import Audio
from processor import Processor
from player import Player
from visualizer import Visualizer


audio = Audio(channels=1, rate=44100, chunk=1024)


processor = Processor()
processor.start()

player = Player(processor.event_bus)
visualizer = Visualizer(audio.chunk, audio.channels, scale=4)
with audio.generate(player.on_tick) as stream:
    while stream.is_active():
        if not stream.empty():
            visualizer.update(stream.get())
