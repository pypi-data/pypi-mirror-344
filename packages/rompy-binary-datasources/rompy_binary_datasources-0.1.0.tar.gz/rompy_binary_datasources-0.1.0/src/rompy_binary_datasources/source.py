"""
Binary data source classes for rompy.

This module contains source classes that handle binary data formats like
pandas DataFrames and xarray Datasets that may cause issues with OpenAPI schema generation.
"""

import logging
from typing import Literal, Optional

import pandas as pd
import xarray as xr
from pydantic import ConfigDict, Field, field_validator
from rompy.core.source import SourceBase

logger = logging.getLogger(__name__)


class SourceDataset(SourceBase):
    """Source dataset from an existing xarray Dataset object."""

    model_type: Literal["dataset"] = Field(
        default="dataset",
        description="Model type discriminator",
    )
    obj: xr.Dataset = Field(
        description="xarray Dataset object",
    )
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __str__(self) -> str:
        return f"SourceDataset(obj={self.obj})"

    def _open(self) -> xr.Dataset:
        return self.obj


class SourceTimeseriesDataFrame(SourceBase):
    """Source dataset from an existing pandas DataFrame timeseries object."""

    model_type: Literal["dataframe"] = Field(
        default="dataframe",
        description="Model type discriminator",
    )
    obj: pd.DataFrame = Field(
        description="pandas DataFrame object",
    )
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("obj")
    @classmethod
    def is_timeseries(cls, obj: pd.DataFrame) -> pd.DataFrame:
        """Check if the DataFrame is a timeseries."""
        if not pd.api.types.is_datetime64_any_dtype(obj.index):
            raise ValueError("The DataFrame index must be datetime dtype")
        if obj.index.name is None:
            raise ValueError("The DataFrame index must have a name")
        return obj

    def __str__(self) -> str:
        return f"SourceTimeseriesDataFrame(obj={self.obj})"

    def _open(self) -> xr.Dataset:
        return xr.Dataset.from_dataframe(self.obj).rename({self.obj.index.name: "time"})
