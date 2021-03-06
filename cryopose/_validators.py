from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

import numpy as np
import pandas as pd
from numpy.typing import ArrayLike, NDArray
from pandas.api.types import is_numeric_dtype, is_string_dtype
from scipy.spatial.transform import Rotation

from ._data_labels import CryoPoseDataLabels as CPDL

if TYPE_CHECKING:
    import Literal


def validate_positions(positions: ArrayLike, ndim: Literal[2, 3] = 3) -> NDArray:
    positions = np.asarray(positions, dtype=float)
    if positions.ndim != 2 or positions.shape[1] not in (2, 3):
        raise ValueError(
            f"positions must be a (n, 2) or (n, 3) array, got {positions.shape}"
        )
    if ndim != positions.shape[1]:
        raise ValueError(
            f"positions are {positions.shape[1]}D, but a {ndim}D cryopose was requested"
        )
    return positions


def validate_orientations(
    orientations: Rotation | Sequence[Rotation], ndim: Literal[2, 3] = 3
) -> Rotation:
    return Rotation.concatenate(orientations)


def validate_cryopose_dataframe(
    df: pd.DataFrame, ndim: Literal[2, 3] = 3
) -> pd.DataFrame:
    """Validate a cryopose dataframe."""
    for col in CPDL.POSITION[:ndim]:
        if col not in df:
            raise KeyError(col)
        if not is_numeric_dtype(df[col]):
            raise TypeError(f'dtype of "{col}" should be a Number, got {df[col].dtype}')

    if CPDL.ORIENTATION not in df:
        raise KeyError(CPDL.ORIENTATION)
    # cannot just check dtype, so we have to validate the objects themselves
    if len(df) > 0:
        validate_orientations(df[CPDL.ORIENTATION], ndim=ndim)

    if CPDL.PIXEL_SPACING not in df:
        raise KeyError(CPDL.PIXEL_SPACING)
    if not is_numeric_dtype(df[CPDL.PIXEL_SPACING]):
        raise TypeError(
            f'dtype of "{CPDL.PIXEL_SPACING}" should be a Number, '
            f"got {df[CPDL.PIXEL_SPACING].dtype}"
        )

    if CPDL.EXPERIMENT_ID not in df:
        raise KeyError(CPDL.EXPERIMENT_ID)
    if not is_string_dtype(df[CPDL.EXPERIMENT_ID]):
        raise TypeError(
            f'dtype of "{CPDL.EXPERIMENT_ID}" should be a string, '
            f"got {df[CPDL.EXPERIMENT_ID].dtype}"
        )

    return df
