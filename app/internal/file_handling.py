import numpy
import io
from PIL import Image, UnidentifiedImageError


class InvalidImageFileError(ValueError):
    """
    Custom exception for invalid image file formats.
    """
    # TODO: write tests?
    pass


def translate_file_to_numpy_array(content: bytes) -> numpy.ndarray:
    """
        Converts the raw byte content of an image file into a numpy array.

        Args:
            content (bytes): The raw byte content of an image file. (example: JPEG, PNG)
        Returns:
            numpy.ndarray: The numpy array representation of the image file.
        Raises:
            InvalidImageFileError: The image file format is not supported.
    """
    # Wrap raw byte content to an in-memory binary stream.
    # This allows Pillow to use it like a file without persisting to disk.
    image_stream = io.BytesIO(content)
    try:
        # use a context to ensure the image is properly closed
        with Image.open(image_stream) as img:
            # convert the image object to a numpy array
            return numpy.array(img)
    except UnidentifiedImageError as e:
        # Pillow cannot open the file (example: not a valid image format)
        raise InvalidImageFileError(f"failed to open or convert image {e}")


def write_numpy_array_to_image_file(data: numpy.ndarray, file_name: str) -> str:
    """
        Saves a NumPy array as a PNG image file.

        This function take a NumPy array containing image data, converts it and save it int a Pillow Image object, and saves it to a specified location as a PNG file.

        Args:
            data (numpy.ndarray): The NumPy array representation of the image file.
            file_name (str): The file name of the image file.

        Returns:
            str: The full file path of the image file.
    """
    # convert the numpy array to a Pillow Image object.
    img_data = Image.fromarray(data)
    # Define the full path for the output file, including the directory.
    file_path = f'app/_tmp/{file_name}.png'
    # save the image object to the save location in PNG format
    img_data.save(file_path, 'PNG')
    # return the path where the image was saved
    return file_path
