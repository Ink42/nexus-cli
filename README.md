# Nexus-cli 

> Modable CLI - A Lightweight, Modular Command Line Interface

## Overview

Originally conceived while modding Project Zomboid and exploring Lua, this project evolved into a flexible, modular command line interface framework in Python. Designed for extensibility, it allows users to easily add functionality through plugins while maintaining a lightweight core.

**P.S Note that this current version is a proof of concept.**

### Features

* **Plugin System:** Easily extend functionality by adding Python modules
* **Message Bus Architecture:** Inspired by robust event-driven systems (still in development)
* **YAML Configuration:** For additional flexibility in plugin configuration (still in development)
* **Lightweight Core:** Minimal overhead with maximum extensibility
* **Python-based:** Chosen for its versatility after Dart proved unsuitable

## Installation

1.  **Clone this repository:**

    ```bash
    git clone https://github.com/Ink42/nexus-cli.git
    cd modable-cli
    ```

2.  **Ensure you have Python 3.6+ installed.**

3.  **Install required dependencies:**

    ```bash
    pip install pyyaml
    ```

## Usage

### Basic Usage

```bash
python minicli.py <command> [arguments]
```

## Creating Plugins
Create a new Python file in the modules directory. Define two required components:

- SUBSCRIBE: The command name (string)
- handle(args): The function that processes command arguments

Example plugin (modules/echo.py):


```
SUBSCRIBE = "echo"

def handle(args):
    print(f"[echo plugin] {args}")
```


Run a plugin command:

```
python minicli.py echo "Hello World"
```

## Contributing

Contributions are welcome! Please:

- Fork the repository.
- Create a feature branch.
- Submit a pull request.

## License

- MIT License

Built when stuck on another project, this CLI represents the best outcome from researching message bus systems and configuration flexibility - proving that sometimes the best solutions come from unexpected places.
