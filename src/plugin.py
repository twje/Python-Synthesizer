class Plugin:
    def __init__(self):
        self.plugins = []

    def prime_plugins(self, data):
        for plugin in self.plugins:
            plugin.stream.put(data)

    def update_plugins(self):
        for plugin in self.plugins:
            plugin.update()

    def add_plugin(self, plugin):
        self.plugins.append(plugin)
