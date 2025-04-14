import unittest
from unittest.mock import patch, mock_open, MagicMock
import importlib.util
import sys
import os
from io import StringIO


import minicli

class TestMinicli(unittest.TestCase):
    def setUp(self):
        self.original_argv = sys.argv
        self.original_modules_dir = minicli.MODULES_DIR
        self.original_stdout = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        sys.argv = self.original_argv
        minicli.MODULES_DIR = self.original_modules_dir
        sys.stdout = self.original_stdout

    @patch('os.listdir')
    @patch('importlib.util.spec_from_file_location')
    @patch('importlib.util.module_from_spec')
    def test_load_plugins(self, mock_module_from_spec, mock_spec_from_file, mock_listdir):
        mock_listdir.return_value = ['echo.py', 'test.py', 'invalid.txt']
        minicli.MODULES_DIR = 'mocked_modules'
        
     
        mock_echo_module = MagicMock()
        mock_echo_module.SUBSCRIBE = "echo"
        mock_echo_module.handle = MagicMock()
        

        mock_test_module = MagicMock()
        mock_test_module.SUBSCRIBE = None
        mock_test_module.handle = MagicMock()
        
    
        mock_spec_from_file.side_effect = [
            MagicMock(loader=MagicMock()),  
            MagicMock(loader=MagicMock()),   
        ]
        mock_module_from_spec.side_effect = [mock_echo_module, mock_test_module]
        
      
        plugins = minicli.load_plugins()
        

        self.assertEqual(len(plugins), 1)
        self.assertIn("echo", plugins)
        self.assertEqual(plugins["echo"], mock_echo_module.handle)

    @patch('minicli.load_plugins')
    def test_main_with_valid_command(self, mock_load_plugins):
        
        sys.argv = ['minicli', 'echo', 'test argument']
        mock_load_plugins.return_value = {'echo': MagicMock()}
        minicli.main()
        output = sys.stdout.getvalue()
        self.assertIn("[minicli] Routing to: echo", output)

if __name__ == '__main__':
    unittest.main()