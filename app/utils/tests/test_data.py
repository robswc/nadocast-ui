import os
from datetime import datetime

import pytest

from utils.data import get_forecasts, download_forecast


@pytest.mark.skip(reason="Data server is not available")
def test_get_forecasts():
    """Test that we can get forecasts from the data server"""
    forecast = get_forecasts(date=datetime(2024, 5, 7))[0]
    assert forecast is not None


@pytest.mark.skip(reason="Data server is not available")
def test_download_forecast():
    """Test that we can download a forecast from the data server"""
    forecast = get_forecasts(date=datetime(2024, 5, 7))[0]
    file_path = download_forecast(forecast, to_path="storage")
    assert file_path is not None
    assert os.path.exists(file_path)
    os.remove(file_path)
    assert not os.path.exists(file_path)
