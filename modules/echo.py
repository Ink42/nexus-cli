from plugin_base import Plugin

class EchoPlugin(Plugin):
    SUBSCRIBE = "echo"

    def handle(self, args):
        print(f"[echo plugin] {args}")
