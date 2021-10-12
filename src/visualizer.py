import struct
import matplotlib.pyplot as plt
import numpy as np


class Visualizer:
    def __init__(self, chunk, channels, scale=1):
        self.x_length = chunk * scale
        self.chunk = chunk
        self.channels = channels
        self.x = np.arange(0, self.x_length)
        self.y = np.zeros(self.x_length)
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot(self.x, self.y, 'r')
        self.ax.set_ylim(-6000, 6000)
        self.ax.set_xlim(0, self.x_length)
        self.fig.show()

    def update(self, data):
        data = struct.unpack(str(self.chunk * self.channels) + 'h', data)
        self.y = np.concatenate((self.y, data))[-self.x_length::]
        self.line.set_ydata(self.y)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
