# tests/test_utils.py

import os
import pytest
import unittest.mock as mock
from multirex.utils import get_stellar_phoenix, get_gases, list_gases
from taurex.cache import OpacityCache

# Mock tests to avoid actual downloads during testing

def test_get_stellar_phoenix_existing_directory():
    # Test when Phoenix directory already exists
    with mock.patch('os.path.exists', return_value=True):
        with mock.patch('os.path.join', return_value='mocked/path/Phoenix'):
            with mock.patch('builtins.print') as mock_print:
                result = get_stellar_phoenix('test_path')
                mock_print.assert_called_once()
                assert 'already exists' in mock_print.call_args[0][0]
                assert result == 'mocked/path/Phoenix'

def test_get_stellar_phoenix_new_directory():
    # Test when Phoenix directory doesn't exist and needs to be downloaded
    with mock.patch('os.path.exists', return_value=False):
        with mock.patch('os.path.join', return_value='mocked/path/Phoenix'):
            with mock.patch('gdown.download') as mock_download:
                with mock.patch('zipfile.ZipFile'):
                    with mock.patch('os.remove'):
                        with mock.patch('builtins.print'):
                            result = get_stellar_phoenix('test_path')
                            mock_download.assert_called_once()
                            assert result == 'mocked/path/Phoenix'

def test_get_gases_existing_directory():
    # Test when opacity database directory already exists
    with mock.patch('os.path.exists', return_value=True):
        with mock.patch('os.path.join', return_value='mocked/path/opacidades-todas'):
            with mock.patch('builtins.print') as mock_print:
                with mock.patch.object(OpacityCache, 'clear_cache'):
                    with mock.patch.object(OpacityCache, 'set_opacity_path'):
                        get_gases('test_path')
                        mock_print.assert_called_once()
                        assert 'already exists' in mock_print.call_args[0][0]

def test_get_gases_new_directory():
    # Test when opacity database directory doesn't exist and needs to be downloaded
    with mock.patch('os.path.exists', side_effect=[False, False]):
        with mock.patch('os.path.join', return_value='mocked/path/opacidades-todas'):
            with mock.patch('gdown.download') as mock_download:
                with mock.patch('zipfile.ZipFile'):
                    with mock.patch('os.remove'):
                        with mock.patch('builtins.print'):
                            with mock.patch.object(OpacityCache, 'clear_cache'):
                                with mock.patch.object(OpacityCache, 'set_opacity_path'):
                                    get_gases('test_path')
                                    mock_download.assert_called_once()

def test_list_gases():
    # Test listing available gases
    mock_molecules = ['H2O', 'CO2', 'CH4', 'O3']
    with mock.patch.object(OpacityCache, 'find_list_of_molecules', return_value=mock_molecules):
        with mock.patch('builtins.print') as mock_print:
            list_gases()
            assert mock_print.call_count == 2  # Two print calls in the function
            # Check that the second print call contains the list of molecules
            assert mock_print.call_args_list[1][0][0] == mock_molecules