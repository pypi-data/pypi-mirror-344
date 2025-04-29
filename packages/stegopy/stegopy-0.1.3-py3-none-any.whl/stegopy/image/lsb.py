from stegopy.image import _core

def encode(image_path: str, output_path: str, message: str) -> None:
    """
    Encodes a UTF-8 message into the least significant bits of an image.

    Args:
        image_path (str): Path to the input image file.
        output_path (str): Path where the stego image will be saved.
        message (str): Message to embed.

    Raises:
        FileNotFoundError: If input image does not exist.
        UnsupportedFormatError: If image cannot be read or is invalid.
        PayloadTooLargeError: If message exceeds capacity.
    """
    _core.encode(image_path, output_path, message)

def decode(image_path: str) -> str:
    """
    Decodes a UTF-8 message from the least significant bits of an image.

    Args:
        image_path (str): Image file containing stego data.

    Returns:
        str: Decoded message string.

    Raises:
        FileNotFoundError: If file does not exist.
        UnsupportedFormatError: If image format is invalid.
        InvalidStegoDataError: If message is corrupted or incomplete.
    """
    return _core.decode(image_path)
