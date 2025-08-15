import numpy
import io
from PIL import Image


class InvalidImageFileError(ValueError):
    """
    Custom exception for invalid image file formats.
    """
    pass


def translate_file_to_numpy_array(content: bytes) -> numpy.ndarray:
    """
        TODO: create docstring
    """
    # TODO: comment this code
    image_stream = io.BytesIO(content)
    try:
        with Image.open(image_stream) as img:
            return numpy.array(img)
    except Exception as e:
        raise InvalidImageFileError(f"failed to open or convert image {e}")
