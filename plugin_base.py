# plugin_base.py

class Plugin:
    SUBSCRIBE = None
    DESCRIPTION = "No description provided."

    def handle(self, args):
        raise NotImplementedError("Plugin must implement handle()")

    def get_parser(self):
        # Optional: Plugins can override this to return an argparse parser
        return None
