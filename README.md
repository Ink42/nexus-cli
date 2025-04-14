Modable CLI - A Lightweight, Modular Command Line Interface
Overview
Originally conceived while modding Project Zomboid and exploring Lua, this project evolved into a flexible, modular command line interface framework in Python. Designed for extensibility, it allows users to easily add functionality through plugins while maintaining a lightweight core.

Features
Plugin System: Easily extend functionality by adding Python modules

Message Bus Architecture: Inspired by robust event-driven systems

YAML Configuration: For additional flexibility in plugin configuration

Lightweight Core: Minimal overhead with maximum extensibility

Python-based: Chosen for its versatility after Dart proved unsuitable

Installation
Clone this repository:

bash
Copy
git clone https://github.com/yourusername/modable-cli.git
cd modable-cli
Ensure you have Python 3.6+ installed

Install required dependencies:

bash
Copy
pip install pyyaml
Usage
Basic Usage
bash
Copy
python minicli.py <command> [arguments]
Creating Plugins
Create a new Python file in the modules directory

Define two required components:

SUBSCRIBE: The command name (string)

handle(args): The function that processes command arguments

Example plugin (modules/echo.py):

python
Copy
SUBSCRIBE = "echo"

def handle(args):
    print(f"[echo plugin] {args}")
Available Commands
List all available commands:

bash
Copy
python minicli.py help
Run a plugin command:

bash
Copy
python minicli.py echo "Hello World"
Development Roadmap
Plugin dependency management

Plugin configuration via YAML

Plugin auto-discovery from external sources

Command history and suggestions

Tab completion

Why Python?
After experimenting with Dart and Lua, Python was chosen for:

Rich standard library

Easy module system

Strong community support

Balance between performance and development speed

Contributing
Contributions are welcome! Please:

Fork the repository

Create a feature branch

Submit a pull request

License
MIT License

"Built when stuck on another project, this CLI represents the best outcome from researching message bus systems and configuration flexibility - proving that sometimes the best solutions come from unexpected places."