
# plugin_base.py

class Plugin:
    SUBSCRIBE = None

    def handle(self, args):
        raise NotImplementedError("Plugin must implement handle() method")
