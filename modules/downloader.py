import argparse
from plugin_base import Plugin

class DownloaderPlugin(Plugin):
    SUBSCRIBE = "downloader"
    DESCRIPTION = "Simulates downloading a URL."

    def get_parser(self):
        parser = argparse.ArgumentParser(prog="minicli downloader")
        parser.add_argument("url", help="The URL to download")
        parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
        return parser

    def handle(self, args):
        print(f"[downloader plugin] Got URL: {args.url}")
        if args.verbose:
            print("[downloader plugin] Verbose mode on.")
