from plugin_base import Plugin

class DownloaderPlugin(Plugin):
    SUBSCRIBE = "downloader"

    def handle(self, args):
        print(f"[downloader plugin] Got URL: {args}")
