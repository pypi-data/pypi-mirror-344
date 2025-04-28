from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import xarray as xr

import rompy_binary_datasources

HERE = Path(__file__).parent


@pytest.fixture
def mock_dataset():
    """Create a mock xarray Dataset for testing."""
    # Create a simple dataset with time, lat, lon dimensions
    times = pd.date_range("2023-01-01", periods=3, freq="D")
    lats = np.linspace(-10, 10, 3)
    lons = np.linspace(120, 140, 3)

    # Create some test data
    data = np.random.rand(3, 3, 3)  # time, lat, lon

    # Create the dataset
    ds = xr.Dataset(
        data_vars={"temperature": (["time", "lat", "lon"], data, {"units": "celsius"})},
        coords={
            "time": times,
            "lat": lats,
            "lon": lons,
        },
    )
    return ds


@pytest.fixture
def mock_dataframe():
    """Create a mock pandas DataFrame for testing."""
    # Create a simple time series dataframe
    times = pd.date_range("2023-01-01", periods=24, freq="H")
    data = {
        "wind_speed": np.random.rand(24) * 10,
        "wind_direction": np.random.rand(24) * 360,
    }
    df = pd.DataFrame(data, index=times)
    df.index.name = "time"
    return df


def test_source_dataset(mock_dataset):
    """Test SourceDataset with a mock dataset."""
    source = rompy_binary_datasources.source.SourceDataset(obj=mock_dataset)
    result = source.open()
    assert isinstance(result, xr.Dataset)
    assert "temperature" in result.data_vars
    assert list(result.dims) == ["time", "lat", "lon"]


def test_source_dataframe(mock_dataframe):
    """Test SourceTimeseriesDataFrame with a mock dataframe."""
    source = rompy_binary_datasources.source.SourceTimeseriesDataFrame(
        obj=mock_dataframe
    )
    result = source.open()
    assert isinstance(result, xr.Dataset)
    assert list(result.dims) == ["time"]
    assert "wind_speed" in result.data_vars
    assert "wind_direction" in result.data_vars
