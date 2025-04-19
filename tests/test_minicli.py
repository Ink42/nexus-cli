import sys
import pytest
from unittest.mock import patch
import argparse

from minicli import load_plugins, show_help, scaffold_plugin, main

@pytest.fixture
def plugin_env(tmpdir, monkeypatch):
    plugin_base = tmpdir.join("plugin_base.py")
    plugin_base.write("class Plugin: pass")
    modules_dir = tmpdir.mkdir("modules")
    monkeypatch.syspath_prepend(str(tmpdir))
    monkeypatch.setattr('minicli.MODULES_DIR', str(modules_dir))
    return modules_dir

def test_load_plugins_no_plugins(plugin_env):
    plugins = load_plugins()
    assert plugins == {}

def test_load_plugins_single_plugin(plugin_env):
    test_plugin = plugin_env.join("test.py")
    test_plugin.write('''
from plugin_base import Plugin

class TestPlugin(Plugin):
    SUBSCRIBE = "test"
    DESCRIPTION = "Test plugin"

    def get_parser(self):
        return None

    def handle(self, args):
        pass
''')
    plugins = load_plugins()
    assert "test" in plugins
    assert plugins["test"].DESCRIPTION == "Test plugin"

def test_load_plugins_skips_base_class(plugin_env):
    test_plugin = plugin_env.join("test.py")
    test_plugin.write('''
from plugin_base import Plugin

Plugin.SUBSCRIBE = "base"
Plugin.DESCRIPTION = "Base plugin"
''')
    plugins = load_plugins()
    assert "base" not in plugins

def test_scaffold_plugin_creates_file(plugin_env):
    scaffold_plugin("test")
    expected_file = plugin_env.join("test.py")
    assert expected_file.exists()
    content = expected_file.read()
    assert "class TestPlugin(Plugin):" in content
    assert 'SUBSCRIBE = "test"' in content

def test_scaffold_plugin_existing_file(plugin_env, capsys):
    existing_file = plugin_env.join("test.py")
    existing_file.write("existing content")
    scaffold_plugin("test")
    captured = capsys.readouterr()
    assert "[scaffold] Plugin 'test' already exists." in captured.out
    assert existing_file.read() == "existing content"



def test_main_no_arguments(capsys, monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['minicli'])
    main()
    captured = capsys.readouterr()
    assert "Available commands:" in captured.out

def test_main_scaffold_command(plugin_env, capsys, monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['minicli', 'scaffold', 'newplugin'])
    main()
    captured = capsys.readouterr()
    assert "[scaffold] Created plugin: modules/newplugin.py" in captured.out
    assert plugin_env.join("newplugin.py").exists()

def test_main_scaffold_missing_name(capsys, monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['minicli', 'scaffold'])
    main()
    captured = capsys.readouterr()
    assert "Usage: minicli scaffold <plugin_name>" in captured.out

def test_main_unknown_command(capsys, monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['minicli', 'unknown'])
    # Mock load_plugins to return no plugins
    with patch('minicli.load_plugins', return_value={}):
        main()
    captured = capsys.readouterr()
    assert "[minicli] Unknown command: unknown" in captured.out

def test_main_plugin_command(plugin_env, capsys, monkeypatch):
    plugin_env.join("test.py").write('''
from plugin_base import Plugin

class TestPlugin(Plugin):
    SUBSCRIBE = "test"
    DESCRIPTION = "Test plugin"

    def get_parser(self):
        return None

    def handle(self, args):
        print("Handled:", args)
''')
    monkeypatch.setattr(sys, 'argv', ['minicli', 'test', 'arg1'])
    main()
    captured = capsys.readouterr()
    assert "Handled: arg1" in captured.out

def test_main_plugin_with_parser(plugin_env, capsys, monkeypatch):
    plugin_env.join("test.py").write('''
from plugin_base import Plugin
import argparse

class TestPlugin(Plugin):
    SUBSCRIBE = "test"
    DESCRIPTION = "Test plugin"

    def get_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--option')
        return parser

    def handle(self, args):
        print(f"Option: {args.option}")
''')
    monkeypatch.setattr(sys, 'argv', ['minicli', 'test', '--option', 'value'])
    main()
    captured = capsys.readouterr()
    assert "Option: value" in captured.out

def test_main_plugin_help(plugin_env, capsys, monkeypatch):
    plugin_env.join("test.py").write('''
from plugin_base import Plugin
import argparse

class TestPlugin(Plugin):
    SUBSCRIBE = "test"
    DESCRIPTION = "Test plugin"

    def get_parser(self):
        parser = argparse.ArgumentParser(prog='minicli test')
        parser.add_argument('--option', help='an option')
        return parser

    def handle(self, args):
        pass
''')
    monkeypatch.setattr(sys, 'argv', ['minicli', 'test', '--help'])
    try:
        main()
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert "usage: minicli test" in captured.out

def test_main_plugin_no_parser_help(plugin_env, capsys, monkeypatch):
    plugin_env.join("test.py").write('''
from plugin_base import Plugin

class TestPlugin(Plugin):
    SUBSCRIBE = "test"
    DESCRIPTION = "Test plugin"

    def get_parser(self):
        return None

    def handle(self, args):
        pass
''')
    monkeypatch.setattr(sys, 'argv', ['minicli', 'test', '--help'])
    main()
    captured = capsys.readouterr()
    assert "test: Test plugin" in captured.out


## Ignore just wanna check see the workflow pass