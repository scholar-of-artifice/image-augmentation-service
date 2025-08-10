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


def test_shift_invalid_direction():
    """
    GIVEN a 4x4 matrix
    AND the direction is not a valid direction
    AND the distance is 3
    WHEN shift is called
    THEN the new matrix has the correct value
    """
    input_image = numpy.array([[1, 0, 0, 0],
                               [0, 2, 0, 0],
                               [0, 0, 3, 0],
                               [0, 0, 0, 4]])
    expected_output = numpy.array([[1, 0, 0, 0],
                                   [0, 2, 0, 0],
                                   [0, 0, 3, 0],
                                   [0, 0, 0, 4]])
    calculated_output = shift(input_image, 'whichaway', 3)
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


def test_rotate_example_90_degrees():
    """
    GIVEN a 11x11 matrix
    AND the amount is 90 degrees
    WHEN rotate is called
    THEN the new matrix has the correct value
    """
    input_image = numpy.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11]])
    expected_output = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    calculated_output = rotate(input_image, 90)
    assert numpy.array_equal(calculated_output, expected_output)
