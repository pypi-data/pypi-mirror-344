"""OpenDAP Catalog Data classes."""

from __future__ import annotations

from typing import Any, Optional

import numpy as np
from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator, model_validator


class CatClimRItem(BaseModel):
    """Mike Johnson's CatClimRItem class.

    Source data from:
    'https://github.com/mikejohnson51/climateR-catalogs/releases/download/June-2024/catalog.parquet'
    """

    id: Optional[str] = None
    asset: Optional[str] = None
    URL: str
    varname: str
    long_name: Optional[str] = None
    variable: Optional[str] = None
    description: Optional[str] = None
    units: Optional[str] = None
    model: Optional[str] = None
    ensemble: Optional[str] = None
    scenario: Optional[str] = None
    T_name: Optional[str] = None
    duration: Optional[str] = None
    interval: Optional[str] = None
    nT: Optional[int] = Field(default=0)  # noqa: N815
    X_name: str
    Y_name: str
    X1: Optional[float] = None
    Xn: Optional[float] = None
    Y1: Optional[float] = None
    Yn: Optional[float] = None
    resX: float  # noqa: N815
    resY: float  # noqa: N815
    ncols: Optional[int] = None
    nrows: Optional[int] = None
    proj: Optional[str] = None
    toptobottom: bool
    tiled: Optional[str] = None
    crs: Optional[str] = None

    @model_validator(mode="after")
    def set_default_long_name(self, info: ValidationInfo) -> "CatClimRItem":
        """Set `long_name` from `description` if missing."""
        if not self.long_name:
            self.long_name = self.description or "None"
        return self

    @model_validator(mode="after")
    def _set_proj(self, info: ValidationInfo) -> "CatClimRItem":
        """Set `proj` from `crs` if `proj` is missing."""
        if not self.proj:
            self.proj = self.crs or "EPSG:4326"
        return self

    @field_validator("nT", mode="before", check_fields=False)
    @classmethod
    def set_nt(cls, v: Any) -> int:
        """Convert nT to int, handle NaN."""
        if v is None:
            return 0
        if isinstance(v, (float, np.floating)) and np.isnan(v):
            return 0
        return int(v)

    @field_validator("toptobottom", mode="before")
    @classmethod
    def _toptobottom_as_bool(cls, v: Any) -> bool:
        """Convert 'TRUE'/'FALSE' strings to real boolean True/False."""
        if isinstance(v, str):
            return v.strip().upper() == "TRUE"
        return bool(v)

    @field_validator("tiled", mode="before", check_fields=False)
    @classmethod
    def _tiled(cls, val: Optional[str]) -> str:
        """Ensure tiled value is valid."""
        if not val:
            return "NA"
        val = val.upper()
        if val not in ["", "NA", "T", "XY"]:
            raise ValueError("tiled must be one of ['', 'NA', 'T', 'XY']")
        return val

    model_config = ConfigDict(
        str_strip_whitespace=False,
        frozen=False,  # allow mutation (new way)
    )
