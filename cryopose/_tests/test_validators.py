import numpy as np
import pytest

from cryopose._validators import validate_positions


def test_position_validator():
    pos3d = np.random.rand(10, 3)
    valid = validate_positions(pos3d, 3)
    assert valid.shape == (10, 3)

    with pytest.raises(ValueError):
        validate_positions(pos3d, 2)

    pos2d = np.random.rand(10, 2)
    valid = validate_positions(pos2d, 2)
    assert valid.shape == (10, 2)

    with pytest.raises(ValueError):
        validate_positions(pos2d, 3)

    wrong = np.random.rand(10, 4)
    with pytest.raises(ValueError):
        validate_positions(wrong, 2)
    with pytest.raises(ValueError):
        validate_positions(wrong, 3)
