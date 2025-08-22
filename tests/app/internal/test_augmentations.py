import numpy
import pytest
from app.internal.augmentations import shift, rotate


@pytest.mark.parametrize("direction, distance, expected_output", [
    ('up', 2, numpy.array([[0, 0, 3, 0,],
                           [0, 0, 0, 4,],
                           [1, 0, 0, 0,],
                           [0, 2, 0, 0,]])),
    ('down', 2, numpy.array([[0, 0, 3, 0],
                             [0, 0, 0, 4],
                             [1, 0, 0, 0],
                             [0, 2, 0, 0]])),
    ('left', 2, numpy.array([[0, 0, 1, 0],
                             [0, 0, 0, 2],
                             [3, 0, 0, 0],
                             [0, 4, 0, 0]])),
    ('right', 2, numpy.array([[0, 0, 1, 0],
                              [0, 0, 0, 2],
                              [3, 0, 0, 0],
                              [0, 4, 0, 0]])),
])
def test_shift_produces_correct_results(direction, distance, expected_output):
    """
    GIVEN a 4x4 matrix
    AND the input arguments
    WHEN shift is called
    THEN the new matrix has the correct value
    """
    input_image = numpy.array([[1, 0, 0, 0],
                               [0, 2, 0, 0],
                               [0, 0, 3, 0],
                               [0, 0, 0, 4]])
    calculated_output = shift(image_data=input_image,
                              direction=direction, distance=distance)
    print(calculated_output)
    assert numpy.array_equal(calculated_output, expected_output)


def test_shift_invalid_direction_raises_exception():
    """
    GIVEN a 4x4 matrix
    AND the direction is not a valid direction
    AND the distance is 3
    WHEN shift is called
    THEN it raises a ValueError
    """
    input_image = numpy.array([[1, 0, 0, 0],
                               [0, 2, 0, 0],
                               [0, 0, 3, 0],
                               [0, 0, 0, 4]])
    with pytest.raises(ValueError):
        shift(input_image, 'whichaway', 3)


def test_shift_None_direction_raises_exception():
    """
    GIVEN a 4x4 matrix
    AND the direction is None
    AND the distance is 3
    WHEN shift is called
    THEN it raises a TypeError
    """
    input_image = numpy.array([[1, 0, 0, 0],
                               [0, 2, 0, 0],
                               [0, 0, 3, 0],
                               [0, 0, 0, 4]])
    with pytest.raises(TypeError):
        shift(input_image, None, 3)


def test_shift_blank_string_direction_raises_exception():
    """
    GIVEN a 4x4 matrix
    AND the direction is a blank string
    AND the distance is 3
    WHEN shift is called
    THEN it raises a ValueError
    """
    input_image = numpy.array([[1, 0, 0, 0],
                               [0, 2, 0, 0],
                               [0, 0, 3, 0],
                               [0, 0, 0, 4]])
    with pytest.raises(ValueError):
        shift(input_image, '', 3)


def test_shift_float_distance_raises_exception():
    """
    GIVEN a 4x4 matrix
    AND the direction is a blank string
    AND the distance is 3.5
    WHEN shift is called
    THEN it raises a TypeError
    """
    input_image = numpy.array([[1, 0, 0, 0],
                               [0, 2, 0, 0],
                               [0, 0, 3, 0],
                               [0, 0, 0, 4]])
    with pytest.raises(TypeError):
        shift(input_image, 'up', 3.5)

def test_shift_bad_input_dimensions_raises_exception():
    """
    GIVEN a 4x4 matrix
    AND the input dimensions are incorrect
    WHEN shift is called
    THEN it raises a TypeError
    """
    input_image = numpy.array([1, 0, 0, 0])
    with pytest.raises(TypeError):
        shift(input_image, 'left', 3)


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
