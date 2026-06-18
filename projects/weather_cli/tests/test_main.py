import pytest
from unittest.mock import patch, MagicMock
from main import get_weather

@patch('requests.get')
def test_get_weather_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    
    weather = get_weather("London")
    assert weather['temp'] == 15
    assert weather['condition'] == "Cloudy"

@patch('requests.get')
def test_get_weather_failure(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response
    
    with pytest.raises(ConnectionError):
        get_weather("London")
