import numpy
import io
from PIL import Image, UnidentifiedImageError
import uuid
from pathlib import Path

# Define the mapping from volume names to the in-container paths
VOLUME_PATHS = {
    "unprocessed_image_data": Path("/app/images/unprocessed"),
    "processed_image_data": Path("/app/images/processed"),
}

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


def write_numpy_array_to_image_file(data: numpy.ndarray, file_name: str, destination_volume: str) -> str:
    """
        Saves a NumPy array as a PNG image file.

        This function take a NumPy array containing image data, converts it and save it int a Pillow Image object, and saves it to a specified location as a PNG file.

        Args:
            data (numpy.ndarray): The NumPy array representation of the image file.
            file_name (str): The file name of the image file.
            destination_volume (str): The volume where the image file will be saved. (example: unprocessed_image_data)

        Returns:
            str: The full file path of the image file.
    """
    # look up the base path for the destination volume
    base_path = VOLUME_PATHS.get(destination_volume)
    if not base_path:
        raise ValueError(f"Invalid destination volume: {destination_volume}")
    # ensure the destination directory exists
    base_path.mkdir(parents=True, exist_ok=True)
    # define the full path for the output file, including the directory.
    file_path = base_path / Path(file_name).with_suffix(suffix= ".png")
    # convert the numpy array to a Pillow Image object.
    img_data = Image.fromarray(data)
    # save the image object to the save location in PNG format
    img_data.save(fp= file_path, format='PNG')
    # return the path where the image was saved
    return str(file_path)

def create_file_name() -> str:
    """
    Generates a unique file name for the image file.
    """
    return str(uuid.uuid4())
