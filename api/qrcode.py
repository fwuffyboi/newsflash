import base64
from io import BytesIO


def make_qr_code(data: str, size: int = 100) -> bytes:
    """
    Generate a QR code image from the given data.

    Args:
        data (str): The data to encode in the QR code.
        size (int): The size of the QR code. Default is 10.

    Returns:
        bytes: The generated PNG image of the QR code in base64 format.
    """
    import qrcode
    import base64
    from io import BytesIO

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=0,  # No border
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())

    return img_str