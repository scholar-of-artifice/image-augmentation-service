import numpy
import io
from PIL import Image


class InvalidImageFileError(ValueError):
    """
    Custom exception for invalid image file formats.
    """
    # TODO: write tests?
    pass


def translate_file_to_numpy_array(content: bytes) -> numpy.ndarray:
    """
        TODO: create docstring
    """
    # TODO: comment this code
    # TODO: write tests
    image_stream = io.BytesIO(content)
    try:
        with Image.open(image_stream) as img:
            return numpy.array(img)
    except Exception as e:
        raise InvalidImageFileError(f"failed to open or convert image {e}")


def write_numpy_array_to_image_file(data: numpy.ndarray, file_name: str) -> str:
    """
        TODO: create docstring
    """
    # TODO: comment this code
    img_data = Image.fromarray(data)
    # TODO: change write location
    file_path = 'app/_tmp/' + file_name + '.png'
    img_data.save('app/_tmp/' + file_name + '.png', 'PNG')
    # TODO: change what is returned
    return file_path
