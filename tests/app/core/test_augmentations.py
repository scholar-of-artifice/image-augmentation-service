import numpy
import pytest
from app.core.augmentations import shift


def test_shift_up():
    """
    GIVEN a 4x4 matrix
    AND the direction is up
    AND the distance is 2
    WHEN shift is called
    THEN the new matrix has the correct value
    """
    input_image = numpy.array([[1, 0, 0, 0],
                               [0, 2, 0, 0],
                               [0, 0, 3, 0],
                               [0, 0, 0, 4]])
    expected_output = numpy.array([[0, 0, 3, 0],
                                   [0, 0, 0, 4],
                                   [1, 0, 0, 0],
                                   [0, 2, 0, 0]])
    calculated_output = shift(input_image, 'up', 2)
    assert numpy.array_equal(calculated_output, expected_output)
