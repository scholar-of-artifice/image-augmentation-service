import numpy
import pytest
from app.core.augmentations import shift, rotate


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


def test_shift_down():
    """
    GIVEN a 4x4 matrix
    AND the direction is down
    AND the distance is 3
    WHEN shift is called
    THEN the new matrix has the correct value
    """
    input_image = numpy.array([[1, 0, 0, 0],
                               [0, 2, 0, 0],
                               [0, 0, 3, 0],
                               [0, 0, 0, 4]])
    expected_output = numpy.array([[0, 2, 0, 0],
                                   [0, 0, 3, 0],
                                   [0, 0, 0, 4],
                                   [1, 0, 0, 0]])
    calculated_output = shift(input_image, 'down', 3)
    assert numpy.array_equal(calculated_output, expected_output)


def test_shift_left():
    """
    GIVEN a 4x4 matrix
    AND the direction is left
    AND the distance is 2
    WHEN shift is called
    THEN the new matrix has the correct value
    """
    input_image = numpy.array([[1, 0, 0, 0],
                               [0, 2, 0, 0],
                               [0, 0, 3, 0],
                               [0, 0, 0, 4]])
    expected_output = numpy.array([[0, 0, 1, 0],
                                   [0, 0, 0, 2],
                                   [3, 0, 0, 0],
                                   [0, 4, 0, 0]])
    calculated_output = shift(input_image, 'left', 2)
    assert numpy.array_equal(calculated_output, expected_output)


def test_shift_right():
    """
    GIVEN a 4x4 matrix
    AND the direction is right
    AND the distance is 3
    WHEN shift is called
    THEN the new matrix has the correct value
    """
    input_image = numpy.array([[1, 0, 0, 0],
                               [0, 2, 0, 0],
                               [0, 0, 3, 0],
                               [0, 0, 0, 4]])
    expected_output = numpy.array([[0, 0, 0, 1],
                                   [2, 0, 0, 0],
                                   [0, 3, 0, 0],
                                   [0, 0, 4, 0]])
    calculated_output = shift(input_image, 'right', 3)
    assert numpy.array_equal(calculated_output, expected_output)


def test_rotate_example_45_degrees():
    """
    GIVEN a 4x4 matrix
    AND the amount is 45 degrees
    WHEN rotate is called
    THEN the new matrix has the correct value
    """
    input_image = numpy.array([[1, 0, 0, 0],
                               [0, 2, 0, 0],
                               [0, 0, 3, 0],
                               [0, 0, 0, 4]])
    expected_output = numpy.array([[0, 0, 0, 0],
                                   [0, 1, 1, 1],
                                   [0, 1, 1, 1],
                                   [0, 0, 0, 0]])
    calculated_output = rotate(input_image, 45)
    assert numpy.array_equal(calculated_output, expected_output)
