# -*- coding: utf-8 -*-
import os
import shutil
import tempfile
import unittest
try:
    from unittest.mock import patch  # py3
except ImportError:
    from mock import patch

from click.testing import CliRunner

from callisto import callisto


@patch('callisto.callisto.kernelspec')
class TestCallisto(unittest.TestCase):
    test_cases = (
        'easy',
        'hard/one with spaces',
        '\o/',
        '¯\\_(ツ)_/¯',
        u'\\u041c\\u0430\\u043a\\u0435\\u0434\\u043e\\u043d\\u0438\\u0458\\u0430',
    )

    @classmethod
    def setUpClass(cls):
        cls.tempdir = tempfile.mkdtemp()

    def setUp(self):
        os.environ[callisto.VIRTUAL_ENV_VAR] = self.tempdir

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tempdir)

    def tearDown(self):
        os.environ.pop(callisto.VIRTUAL_ENV_VAR)

    def test_get_kernel_path(self, mock_kernelspec):
        mock_kernelspec.jupyter_data_dir.return_value = self.tempdir
        for test_case in self.test_cases:
            filename = callisto.get_kernel_path(test_case)
            #  All filenames end with kernel.json
            self.assertTrue(filename.endswith('kernel.json'))

    @patch('callisto.callisto.get_display_name')
    def test_install_kernel(self, mock_get_display_name, mock_kernelspec):
        mock_kernelspec.jupyter_data_dir.return_value = self.tempdir
        for test_case in self.test_cases:
            mock_get_display_name.return_value = test_case
            kernel_path = callisto.get_kernel_path(test_case)
            #  Path is safe to write to
            self.assertTrue(callisto.confirm_kernel_path_is_safe(kernel_path))

            fake_env_path = 'fake_env_path'
            success, kernel, actual_kernel_path = callisto.install_kernel('', fake_env_path)

            #  Patching worked
            self.assertEqual(kernel_path, actual_kernel_path)

            # Great success
            self.assertTrue(success)

            # Added to python path
            self.assertIn(fake_env_path, kernel['env']['PYTHONPATH'])

            #  Path isn't safe any more
            self.assertFalse(callisto.confirm_kernel_path_is_safe(kernel_path))

            #  Data is sort of correct
            self.assertEqual(kernel['display_name'], test_case)

            #  No more success
            success, _, __ = callisto.install_kernel('', fake_env_path)
            self.assertFalse(success)

    @patch('callisto.callisto.get_executable')
    def test_cli(self, mock_executable, mock_kernelspec):
        mock_executable.return_value = 'python'
        mock_kernelspec.jupyter_data_dir.return_value = self.tempdir
        runner = CliRunner()

        result = runner.invoke(callisto.cli)
        self.assertEqual(result.exit_code, 0)

        success, kernel, path = callisto.read_kernel('')
        self.assertTrue(success)
        self.assertIn(self.tempdir, path)

        #  Can also confirm this with '-l'
        result = runner.invoke(callisto.cli, ["-l"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(self.tempdir, result.output)

        result = runner.invoke(callisto.cli, ["-d"])
        self.assertEqual(result.exit_code, 0)
        #  Deleting also echoes the kernel
        self.assertIn(self.tempdir, result.output)

        #  Deleting twice is handled elegantly
        result = runner.invoke(callisto.cli, ["-d"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(callisto.cli, ["-l"])
        self.assertEqual(result.exit_code, 0)
        #  No kernel installed
        self.assertIn('No kernel found', result.output)

        venv_name = 'pete'
        result = runner.invoke(callisto.cli, ["-n", venv_name])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(self.tempdir, result.output)
        self.assertIn(venv_name, result.output)

        result = runner.invoke(callisto.cli, ["-n", venv_name])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Failed", result.output)

        # Exit without status code 0 if used outside of virtual environment
        tmp = os.environ.pop(callisto.VIRTUAL_ENV_VAR)
        result = runner.invoke(callisto.cli)
        self.assertNotEqual(result.exit_code, 0)
        os.environ[callisto.VIRTUAL_ENV_VAR] = tmp
