import numpy

from app.internal.augmentations import (
    brighten,
    channel_swap,
    cutout,
    darken,
    edge_filter,
    flip,
    gaussian_blur,
    invert,
    max_filter,
    pepper_noise,
    percentile_filter,
    rainbow_noise,
    rotate,
    salt_noise,
    shift,
    uniform_blur,
)
from app.schemas.image import AugmentationRequestBody

# map a string in the input parameter to an augmentation function
PROCESSING_MAP = {
    'brighten': brighten,
    'channel_swap': channel_swap,
    'cutout': cutout,
    'darken': darken,
    'edge_filter': edge_filter,
    'shift': shift,
    'rotate': rotate,
    'rainbow_noise': rainbow_noise,
    'salt_noise': salt_noise,
    'pepper_noise': pepper_noise,
    'flip': flip,
}
# TODO: add more functions
# flip
# salt_and_pepper_noise
# blur

async def process_image(
        image_data: numpy.ndarray,
        processing_parameters: AugmentationRequestBody,
) -> numpy.ndarray:
    # get the name of the function to use
    arguments_model = processing_parameters.arguments
    processing_function_name = arguments_model.processing
    # get the actual function object
    processing_function = PROCESSING_MAP[processing_function_name]
    # get the arguments model
    # convert the arguments model to a dictionary but exclude processing field
    kwargs = arguments_model.model_dump(exclude={'processing'})
    # apply the parameters in this request
    new_image = processing_function(image_data, **kwargs)
    # return the new image
    return new_image
