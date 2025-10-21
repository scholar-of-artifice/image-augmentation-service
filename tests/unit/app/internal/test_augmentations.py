import numpy
import pytest

from app.internal.augmentations import (
    brighten,
    channel_swap,
    cutout,
    darken,
    edge_filter,
    flip,
    invert,
    mute_channel,
    pepper_noise,
    rainbow_noise,
    rotate,
    salt_noise,
    shift,
)

# --- brighten ---

def test_brighten_is_correct_for_8_bit_RGB_image():
    """
    GIVEN an 8-bit RGB image
    AND an amount of 50% increase
    WHEN brighten is called
    THEN the brightened image has the correct values
    """
    input_image = numpy.array(
        object= [
            [[255,  128,    0]],
        ], dtype=numpy.uint8
    )
    expected_output = numpy.array(
        object= [
            [[255,  255,    127]],
        ], dtype=numpy.uint8
    )
    calculated_output = brighten(
        image_data=input_image,
        amount=0.5,
    )
    assert numpy.array_equal(calculated_output, expected_output)

# --- channel_swap ---

def test_channel_swap_r_g_is_correct_result():
    """
    GIVEN a 2x2 matrix
    AND we want to swap R <-> G
    WHEN channel_swap is called
    THEN the correct result is computed
    """
    input_image = numpy.array(
        [
            [[255,    0,    0], [0,     255,   0]],
            [[255,  255,    0], [255,   0,   255]],
        ], dtype=numpy.uint8
    )
    expected_result = numpy.array(
        [
            [[0,    255,    0], [255,    0,   0]],
            [[255,  255,    0], [0,    255, 255]],
        ], dtype=numpy.uint8
    )
    calculated_result = channel_swap(input_image, a='r', b='g')
    assert numpy.array_equal(calculated_result, expected_result)


def test_channel_swap_r_b_is_correct_result():
    """
    GIVEN a 2x2 matrix
    AND we want to swap R <-> B
    WHEN channel_swap is called
    THEN the correct result is computed
    """
    input_image = numpy.array(
        [
            [[255,    0,    0], [0,     255,   0]],
            [[255,  255,    0], [255,   0,   255]],
        ], dtype=numpy.uint8
    )
    expected_result = numpy.array(
        [
            [[  0,    0,  255], [0,     255,   0]],
            [[  0,  255,  255], [255,   0,   255]],
        ], dtype=numpy.uint8
    )
    calculated_result = channel_swap(input_image, a='r', b='b')
    assert numpy.array_equal(calculated_result, expected_result)


def test_channel_swap_g_b_is_correct_result():
    """
    GIVEN a 2x2 matrix
    AND we want to swap G <-> B
    WHEN channel_swap is called
    THEN the correct result is computed
    """
    input_image = numpy.array(
        [
            [[255,    0,    0], [0,     255,   0]],
            [[255,  255,    0], [255,   0,   255]],
        ], dtype=numpy.uint8
    )
    expected_result = numpy.array(
        [
            [[255,  0,      0], [  0,     0,   255]],
            [[255,  0,    255], [255,   255,     0]],
        ], dtype=numpy.uint8
    )
    calculated_result = channel_swap(input_image, a='g', b='b')
    assert numpy.array_equal(calculated_result, expected_result)


def test_channel_swap_g_g_is_correct_result():
    """
    GIVEN a 2x2 matrix
    AND we want to swap G <-> G
    WHEN channel_swap is called
    THEN the correct result is computed
    """
    input_image = numpy.array(
        [
            [[255,    0,    0], [0,     255,   0]],
            [[255,  255,    0], [255,   0,   255]],
        ], dtype=numpy.uint8
    )
    expected_result = numpy.array(
        [
            [[255,    0,    0], [0,     255,   0]],
            [[255,  255,    0], [255,   0,   255]],
        ], dtype=numpy.uint8
    )
    calculated_result = channel_swap(input_image, a='g', b='g')
    assert numpy.array_equal(calculated_result, expected_result)

# --- cutout ---

def test_cutout_50_percent_is_correct():
    input_image = numpy.array(
        [
            [[255,  0,      0], [0,     255,  0]],
            [[255,  255,    0], [255,   0,  255]],
        ], dtype=numpy.uint8
    )
    calculated_output = cutout(input_image, amount=0.5)
    # count the number of changed pixels
    number_of_changed_pixels = 0
    for i, row in enumerate(calculated_output):
        for j, pixel in enumerate(row):
            if not numpy.array_equal(pixel, input_image[i, j]):
                number_of_changed_pixels = number_of_changed_pixels + 1
    assert number_of_changed_pixels == 1

# TODO: test contiguous


# --- darken ---

def test_darken_is_correct_for_8_bit_RGB_image():
    """
    GIVEN an 8-bit RGB image
    AND an amount of 50% increase
    WHEN darken is called
    THEN the darekened image has the correct values
    """
    input_image = numpy.array(
        object= [
            [[255,  128,    0]],
        ], dtype=numpy.uint8
    )
    expected_output = numpy.array(
        object= [
            [[127,  0,    0]],
        ], dtype=numpy.uint8
    )
    calculated_output = darken(
        image_data=input_image,
        amount=0.5,
    )
    assert numpy.array_equal(calculated_output, expected_output)

# --- edge_filter ---

# --- flip ---

def test_flip_x_valid_data_is_correct_result():
    """
    GIVEN a 2x2 matrix
    AND the axis is x
    WHEN flip is called
    THEN the correct result is computed
    """
    input_image = numpy.array(
        [
            [[255,  0,      0], [0,     255,  0]],
            [[255,  255,    0], [255,   0,  255]],
        ], dtype=numpy.uint8
    )
    output_image = flip(input_image, axis='x')
    expected_image = numpy.array(
        [
            [[255,  255,    0], [255,   0,  255]],
            [[255,  0,      0], [0,     255,  0]],
        ], dtype=numpy.uint8
    )
    assert numpy.array_equal(output_image, expected_image)

def test_flip_y_valid_data_is_correct_result():
    """
    GIVEN a 2x2 matrix
    AND the axis is y
    WHEN flip is called
    THEN the correct result is computed
    """
    input_image = numpy.array(
        [
            [[255,  0,      0], [0,     255,  0]],
            [[255,  255,    0], [255,   0,  255]],
        ], dtype=numpy.uint8
    )
    output_image = flip(input_image, axis='y')
    expected_image = numpy.array(
        [
            [[0,    255,    0], [255,    0,     0]],
            [[255,    0,  255], [255,  255,     0]],
        ], dtype=numpy.uint8
    )
    assert numpy.array_equal(output_image, expected_image)

# --- gaussian_blur ---

# --- invert ---

def test_invert_produces_correct_results():
    input_image = numpy.array(
        [
            [[255,  0,      0], [0,     255,  0], [0,     0,  255]]
        ], dtype=numpy.uint8
    )
    expected_output = numpy.array(
        [
            [[0,  255,  255], [255,   0, 255], [255, 255,   0]]
        ], dtype=numpy.uint8
    )
    calculated_output = invert(input_image)
    assert numpy.array_equal(calculated_output, expected_output)

# --- max_filter ---

# --- min_filter ---

# --- mute_channel ---

def test_mute_channel_R_produces_correct_results():
    """
    GIVEN an RGB image
    AND a channel of R
    WHEN mute_channel is called
    THEN the correct result is returned
    """
    input_image = numpy.array(
        object= [
            [[255, 255, 255]],
        ]
    )
    calculated_output = mute_channel(
        image_data=input_image,
        channel='r'
    )
    expected_output = numpy.array(
        object= [
            [[0, 255, 255]],
        ]
    )
    assert numpy.array_equal(calculated_output, expected_output)


def test_mute_channel_G_produces_correct_results():
    """
    GIVEN an RGB image
    AND a channel of G
    WHEN mute_channel is called
    THEN the correct result is returned
    """
    input_image = numpy.array(
        object= [
            [[255, 255, 255]],
        ]
    )
    calculated_output = mute_channel(
        image_data=input_image,
        channel='g'
    )
    expected_output = numpy.array(
        object= [
            [[255, 0, 255]],
        ]
    )
    assert numpy.array_equal(calculated_output, expected_output)


def test_mute_channel_B_produces_correct_results():
    """
    GIVEN an RGB image
    AND a channel of B
    WHEN mute_channel is called
    THEN the correct result is returned
    """
    input_image = numpy.array(
        object= [
            [[255, 255, 255]],
        ]
    )
    calculated_output = mute_channel(
        image_data=input_image,
        channel='r'
    )
    expected_output = numpy.array(
        object= [
            [[255, 255, 0]],
        ]
    )
    assert numpy.array_equal(calculated_output, expected_output)

# --- pepper_noise ---

def test_pepper_noise_50_percent_is_correct():
    input_image = numpy.array(
        [
            [[255,  0,      0], [0,     255,  0]],
            [[255,  255,    0], [255,   0,  255]],
        ], dtype=numpy.uint8
    )
    calculated_output = pepper_noise(input_image, amount=0.5)
    # count the number of changed pixels
    number_of_changed_pixels = 0
    for i, row in enumerate(calculated_output):
        for j, pixel in enumerate(row):
            if not numpy.array_equal(pixel, input_image[i, j]):
                number_of_changed_pixels = number_of_changed_pixels + 1
    assert number_of_changed_pixels == 2

# --- percentile_filter ---

# --- rainbow_noise ---


def test_rainbow_noise_example_0_percent():
    """
    GIVEN a 4x4 matrix
    AND the amount is 0%
    WHEN rainbow_noise is called
    THEN the new matrix has the correct value
    """
    input_image = numpy.array(
        [
            [[255,0,0], [0,255,0], [0,0,255], [0,0,0]],
            [[255,255,0], [255,0,255], [0,255,255], [0,0,0]],
            [[255,255,255], [128,128,128], [0,0,0], [0,0,0]],
            [[0,0,0], [0,0,0], [0,0,0], [0,0,0]]
        ], dtype=numpy.uint8
    )
    # this is a random process so we do not check arrays directly
    calculated_output = rainbow_noise(input_image, amount=0.0)
    # count the number of changed pixels
    number_of_changed_pixels = 0
    for i, row in enumerate(calculated_output):
        for j, pixel in enumerate(row):
            if not numpy.array_equal(pixel, input_image[i, j]):
                number_of_changed_pixels = number_of_changed_pixels + 1
    assert number_of_changed_pixels == 0


def test_rainbow_noise_example_25_percent():
    """
    GIVEN a 4x4 matrix
    AND the amount is 25%
    WHEN rainbow_noise is called
    THEN the new matrix has the correct value
    """
    input_image = numpy.array(
        [
            [[255, 0, 0], [0, 255, 0], [0, 0, 255], [0, 0, 0]],
            [[255, 255, 0], [255, 0, 255], [0, 255, 255], [0, 0, 0]],
            [[255, 255, 255], [128, 128, 128], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        ], dtype=numpy.uint8
    )
    # this is a random process so we do not check arrays directly
    calculated_output = rainbow_noise(input_image, amount=0.25)
    # count the number of changed pixels
    number_of_changed_pixels = 0
    for i, row in enumerate(calculated_output):
        for j, pixel in enumerate(row):
            if not numpy.array_equal(pixel, input_image[i, j]):
                number_of_changed_pixels = number_of_changed_pixels + 1
    assert number_of_changed_pixels == 4

def test_rainbow_noise_example_50_percent():
    """
    GIVEN a 4x4 matrix
    AND the amount is 50%
    WHEN rainbow_noise is called
    THEN the new matrix has the correct value
    """
    input_image = numpy.array(
        [
            [[255, 0, 0], [0, 255, 0], [0, 0, 255], [0, 0, 0]],
            [[255, 255, 0], [255, 0, 255], [0, 255, 255], [0, 0, 0]],
            [[255, 255, 255], [128, 128, 128], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        ], dtype=numpy.uint8
    )
    # this is a random process so we do not check arrays directly
    calculated_output = rainbow_noise(input_image, amount=0.5)
    # count the number of changed pixels
    number_of_changed_pixels = 0
    for i, row in enumerate(calculated_output):
        for j, pixel in enumerate(row):
            if not numpy.array_equal(pixel, input_image[i, j]):
                number_of_changed_pixels = number_of_changed_pixels + 1
    assert number_of_changed_pixels == 8

# --- rotate ---

def test_rotate_example_45_degrees():
    """
    GIVEN a 4x4 matrix
    AND the amount is 45 degrees
    WHEN rotate is called
    THEN the new matrix has the correct value
    """
    input_image = numpy.array([[1, 0, 0, 0], [0, 2, 0, 0], [0, 0, 3, 0], [0, 0, 0, 4]])
    expected_output = numpy.array(
        [[0, 0, 0, 0], [0, 1, 1, 1], [0, 1, 1, 1], [0, 0, 0, 0]]
    )
    calculated_output = rotate(input_image, 45)
    assert numpy.array_equal(calculated_output, expected_output)


def test_rotate_example_90_degrees():
    """
    GIVEN a 11x11 matrix
    AND the amount is 90 degrees
    WHEN rotate is called
    THEN the new matrix has the correct value
    """
    input_image = numpy.array(
        [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
        ]
    )
    expected_output = numpy.array(
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
    calculated_output = rotate(input_image, 90)
    assert numpy.array_equal(calculated_output, expected_output)

def test_rotate_example_0_degrees():
    """
    GIVEN a 11x11 matrix
    AND the amount is 0 degrees
    WHEN rotate is called
    THEN the new matrix has the correct value
    """
    input_image = numpy.array(
        [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
        ]
    )
    expected_output = numpy.array(
        [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
        ]
    )
    calculated_output = rotate(input_image, 0)
    assert numpy.array_equal(calculated_output, expected_output)


def test_rotate_bad_input_dimensions_raises_exception():
    """
    GIVEN a 4x4 matrix
    AND the input dimensions are incorrect
    WHEN rotate is called
    THEN it raises a TypeError
    """
    input_image = numpy.array([1, 0, 0, 0])
    with pytest.raises(TypeError):
        rotate(input_image, angle=45)


def test_rotate_angle_of_string_raises_exception():
    """
    GIVEN a 4x4 matrix
    AND the angle is a string
    WHEN rotate is called
    THEN it raises a TypeError
    """
    input_image = numpy.array([[1, 0, 0, 0], [0, 2, 0, 0], [0, 0, 3, 0], [0, 0, 0, 4]])
    with pytest.raises(TypeError):
        rotate(input_image, angle="45")


# --- salt_noise ---

def test_salt_noise_50_percent_is_correct():
    input_image = numpy.array(
        [
            [[255,  0,      0], [0,     255,  0]],
            [[255,  255,    0], [255,   0,  255]],
        ], dtype=numpy.uint8
    )
    calculated_output = salt_noise(input_image, amount=0.5)
    # count the number of changed pixels
    number_of_changed_pixels = 0
    for i, row in enumerate(calculated_output):
        for j, pixel in enumerate(row):
            if not numpy.array_equal(pixel, input_image[i, j]):
                number_of_changed_pixels = number_of_changed_pixels + 1
    assert number_of_changed_pixels == 2

# --- shift ---

@pytest.mark.parametrize(
    "direction, distance, expected_output",
    [
        (
            "up",
            2,
            numpy.array(
                [
                    [
                        0,
                        0,
                        3,
                        0,
                    ],
                    [
                        0,
                        0,
                        0,
                        4,
                    ],
                    [
                        1,
                        0,
                        0,
                        0,
                    ],
                    [
                        0,
                        2,
                        0,
                        0,
                    ],
                ]
            ),
        ),
        (
            "down",
            2,
            numpy.array([[0, 0, 3, 0], [0, 0, 0, 4], [1, 0, 0, 0], [0, 2, 0, 0]]),
        ),
        (
            "left",
            2,
            numpy.array([[0, 0, 1, 0], [0, 0, 0, 2], [3, 0, 0, 0], [0, 4, 0, 0]]),
        ),
        (
            "right",
            2,
            numpy.array([[0, 0, 1, 0], [0, 0, 0, 2], [3, 0, 0, 0], [0, 4, 0, 0]]),
        ),
    ],
)
def test_shift_produces_correct_results(direction, distance, expected_output):
    """
    GIVEN a 4x4 matrix
    AND the input arguments
    WHEN shift is called
    THEN the new matrix has the correct value
    """
    input_image = numpy.array([[1, 0, 0, 0], [0, 2, 0, 0], [0, 0, 3, 0], [0, 0, 0, 4]])
    calculated_output = shift(
        image_data=input_image, direction=direction, distance=distance
    )
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
    input_image = numpy.array([[1, 0, 0, 0], [0, 2, 0, 0], [0, 0, 3, 0], [0, 0, 0, 4]])
    with pytest.raises(ValueError):
        shift(input_image, "whichaway", 3)


def test_shift_None_direction_raises_exception():
    """
    GIVEN a 4x4 matrix
    AND the direction is None
    AND the distance is 3
    WHEN shift is called
    THEN it raises a TypeError
    """
    input_image = numpy.array([[1, 0, 0, 0], [0, 2, 0, 0], [0, 0, 3, 0], [0, 0, 0, 4]])
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
    input_image = numpy.array([[1, 0, 0, 0], [0, 2, 0, 0], [0, 0, 3, 0], [0, 0, 0, 4]])
    with pytest.raises(ValueError):
        shift(input_image, "", 3)


def test_shift_float_distance_raises_exception():
    """
    GIVEN a 4x4 matrix
    AND the direction is a blank string
    AND the distance is 3.5
    WHEN shift is called
    THEN it raises a TypeError
    """
    input_image = numpy.array([[1, 0, 0, 0], [0, 2, 0, 0], [0, 0, 3, 0], [0, 0, 0, 4]])
    with pytest.raises(TypeError):
        shift(input_image, "up", 3.5)


def test_shift_bad_input_dimensions_raises_exception():
    """
    GIVEN a 4x4 matrix
    AND the input dimensions are incorrect
    WHEN shift is called
    THEN it raises a TypeError
    """
    input_image = numpy.array([1, 0, 0, 0])
    with pytest.raises(TypeError):
        shift(input_image, "left", 3)


# --- tint ---

# --- zoom ---