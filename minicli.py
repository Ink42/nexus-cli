import importlib.util
import os
import sys

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

            topic = getattr(module, "SUBSCRIBE", None)
            handler = getattr(module, "handle", None)

            if topic and callable(handler):
                plugins[topic] = handler
    return plugins

def main():
    if len(sys.argv) < 2:
        print("Usage: minicli <command> [args...]")
        return

    command = sys.argv[1]
    args = " ".join(sys.argv[2:])

    plugins = load_plugins()

    if command in plugins:
        print(f"[minicli] Routing to: {command}")
        plugins[command](args)
    else:
        print(f"[minicli] Unknown command: {command}")

if __name__ == "__main__":
    main()
