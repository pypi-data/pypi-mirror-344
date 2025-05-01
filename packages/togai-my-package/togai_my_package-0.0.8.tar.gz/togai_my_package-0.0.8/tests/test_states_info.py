import pytest
import json
from unittest.mock import patch, mock_open
from togai_my_packaging.states_info import is_city_capitol_of_state, slow_add
from pathlib import Path


# Existing tests can remain as they are


@pytest.mark.slow
def test__slow_add():
    """Test `slow_add()`."""
    assert slow_add(1, 2) == 3
    assert slow_add(-1, 1) == 0
    assert slow_add(0, 0) == 0
    assert slow_add(100, 200) == 300


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (5, 5, 10),
        (-5, 5, 0),
        (0, 0, 0),
        (999, 1, 1000),
    ],
)
def test_slow_add_parametrized(a, b, expected):
    """Test slow_add with multiple inputs using parametrize"""
    assert slow_add(a, b) == expected


class TestCapitolCities:
    """Group related tests in a class"""

    def test_nonexistent_city(self):
        """Test with a city that doesn't exist"""
        assert not is_city_capitol_of_state("NonexistentCity", "AnyState")

    @pytest.fixture
    def mock_cities_data(self):
        return [
            {"city": "TestCity", "state": "TestState", "is_capitol": True},
            {"city": "OtherCity", "state": "OtherState", "is_capitol": True},
        ]

    @patch("togai_my_packaging.states_info.CITIES_JSON_FPATH")
    def test_with_mock_data(self, mock_path, mock_cities_data):
        """Test using mocked data"""
        mock_json = json.dumps(mock_cities_data)
        mock_path.read_text.return_value = mock_json

        assert is_city_capitol_of_state("TestCity", "TestState") is True
        assert is_city_capitol_of_state("TestCity", "WrongState") is False


@pytest.mark.edge_cases
def test_edge_cases():
    """Test edge cases like empty strings"""
    assert not is_city_capitol_of_state("", "")
    assert not is_city_capitol_of_state("", "California")
    assert not is_city_capitol_of_state("Sacramento", "")


# # Example of how to mock JSON file read
# @patch("togai_my_packaging.states_info.CITIES_JSON_FPATH.read_text")
# def test_with_mocked_file_read(mock_read_text):
#     """Test with mocked file read operation"""
#     mock_data = '[{"city": "Austin", "state": "Texas", "is_capitol": true}]'
#     mock_read_text.return_value = mock_data

#     assert is_city_capitol_of_state("Austin", "Texas") is True
#     assert is_city_capitol_of_state("Austin", "California") is False
#     assert is_city_capitol_of_state(city_name=city_name, state=state) == is_capitol


# @pytest.mark.slow
# def test__slow_add():
#     """Test `slow_add()`."""
#     assert slow_add(1, 2) == 3
