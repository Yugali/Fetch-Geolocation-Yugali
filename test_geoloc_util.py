import pytest
import requests
from unittest.mock import patch
import json
import os
import time

# Assuming the fetch_geolocation function is imported from geoloc_util.py
from geoloc_util import fetch_geolocation

# Create a mock for the OpenWeather API request to avoid hitting the actual API during tests
@pytest.fixture
def mock_requests_get():
    with patch('requests.get') as mock_get:
        yield mock_get


def test_valid_location(mock_requests_get):
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = {
        'name': 'Madison',
        'sys': {'country': 'US'},
        'coord': {'lat': 43.0748, 'lon': -89.3838}
    }

    fetch_geolocation('Madison, WI')
    mock_requests_get.assert_called_once()
    with open('locations_data.json', 'r') as file:
        data = file.readlines()
        assert len(data) > 0


def test_invalid_location(mock_requests_get):
    mock_requests_get.return_value.status_code = 404
    mock_requests_get.return_value.json.return_value = {'cod': '404', 'message': 'city not found'}

    fetch_geolocation('InvalidCity, XYZ')
    mock_requests_get.assert_called_once()


def test_special_characters(mock_requests_get):
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = {
        'name': 'São Paulo',
        'sys': {'country': 'BR'},
        'coord': {'lat': -23.5505, 'lon': -46.6333}
    }

    fetch_geolocation('São Paulo, Brazil')
    mock_requests_get.assert_called_once()


def test_empty_api_response(mock_requests_get):
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = {}

    fetch_geolocation('Madison, WI')
    mock_requests_get.assert_called_once()


def test_file_write_error(mock_requests_get):
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = {
        'name': 'Tokyo',
        'sys': {'country': 'JP'},
        'coord': {'lat': 35.6895, 'lon': 139.6917}
    }

    # Simulate a file write permission error
    with patch('builtins.open', side_effect=PermissionError("Permission denied")):
        with pytest.raises(PermissionError):
            fetch_geolocation('Tokyo, Japan')


    # Ensure the permission error is caught and handled
    print("Handled file write error")


@pytest.fixture(autouse=True)
def cleanup():
    if os.path.exists('locations_data.json'):
        os.remove('locations_data.json')
    yield
    if os.path.exists('locations_data.json'):
        os.remove('locations_data.json')
