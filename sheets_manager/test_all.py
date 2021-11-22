"""Tests for Sheets class."""
import pytest

from .sheets_manager import Sheets


AS_LIST = [
    ["Name", "Age"],
    ["Fred", 31],
    ["Julie", 28],
]
AS_DICT = [
    {"Name": "Fred", "Age": 31},
    {"Name": "Julie", "Age": 28},
]


def test_to_dict():
    """Test the conversion of sheets-like data to a list of dicts."""
    assert Sheets.to_dict(AS_LIST) == AS_DICT


def test_to_list():
    """Test the conversion of a list of dicts to a sheets-like data."""
    assert Sheets.to_list(AS_DICT) == AS_LIST
    assert Sheets.to_list(AS_DICT, False) == [AS_LIST[1], AS_LIST[2]]


def test_set_data_range():
    """Test that the correct data range is being used."""
    assert Sheets()._set_data_range("test_range") == "test_range"
    assert (
        Sheets(default_range="test_range")._set_data_range("some_other_range")
        == "some_other_range"
    )
    assert Sheets(default_range="test_range")._set_data_range(None) == "test_range"
    with pytest.raises(ValueError, match="No data range provided"):
        Sheets()._set_data_range(None)
