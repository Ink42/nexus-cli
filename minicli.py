import importlib.util
import os
import sys
import argparse
from plugin_base import Plugin

MODULES_DIR = "modules"

def load_plugins():
    plugins = {}
    for filename in os.listdir(MODULES_DIR):
        if filename.endswith(".py"):
            path = os.path.join(MODULES_DIR, filename)
            name = filename[:-3]

            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for attr in dir(module):
                obj = getattr(module, attr)
                if isinstance(obj, type) and issubclass(obj, Plugin) and obj is not Plugin:
                    instance = obj()
                    if instance.SUBSCRIBE:
                        plugins[instance.SUBSCRIBE] = instance
    return plugins

def show_help(plugins):
    print("Available commands:\n")
    for name, plugin in plugins.items():
        print(f"  {name:<12} {plugin.DESCRIPTION}")
    print("\nUse `minicli <command> --help` for plugin-specific help.")

def main():
    plugins = load_plugins()

    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        show_help(plugins)
        return

    command = sys.argv[1]
    plugin_args = sys.argv[2:]

    if command not in plugins:
        print(f"[minicli] Unknown command: {command}")
        show_help(plugins)
        return

    plugin = plugins[command]

    # Check if the plugin provides an argparse parser
    parser = plugin.get_parser()
    if parser:
        try:
            parsed_args = parser.parse_args(plugin_args)
            plugin.handle(parsed_args)
        except SystemExit:
            pass  # argparse already handled the help/usage
    else:
        if "--help" in plugin_args or "-h" in plugin_args:
            print(f"{command}: {plugin.DESCRIPTION}")
        else:
            plugin.handle(" ".join(plugin_args))

if __name__ == "__main__":
    main()
