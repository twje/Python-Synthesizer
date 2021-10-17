from queue import Queue
from visualizer import Visualizer


class VisualizerPlugin:
    def __init__(self, chunk, channels, scale=1):
        self.visualizer = Visualizer(chunk, channels, scale)
        self.stream = Queue()

    def update(self):
        if not self.stream.empty():
            self.visualizer.update(self.stream.get())
