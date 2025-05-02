import qrcode # type: ignore
import datetime
import os
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
# from qrcode.image.styles.colormasks import SquareRootColorMask  # Удалите эту строку, если у вас старая версия qrcode

from typing import Optional

def qrcode_generator(size: int, text: Optional[str] = None, url: Optional[str] = None, contact: Optional[str] = None, color: Optional[str] = None, path: Optional[str] = None) -> None:
    """
    Генерирует обычный QR-код.
    """
    if not any([text, url, contact]):
        raise ValueError("Необходимо указать один из аргументов: text, url, contact.")
    if sum([bool(text), bool(url), bool(contact)]) > 1:
        raise ValueError("Можно указать только один из аргументов: text, url, contact.")

    data = text or url or contact

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Цвета
    if color:
        try:
            background_color, qr_color = map(str.strip, color.split(","))
        except ValueError:
            background_color, qr_color = "#ffffff", "#000000"  # Default if parsing fails
    else:
        background_color, qr_color = "#ffffff", "#000000"  # Default colors

    img = qr.make_image(fill_color=qr_color, back_color=background_color)

    # Размер
    img = img.resize((size, size))

    # Сохранение
    if path:
        img.save(path)
    else:
        # Default filename
        now = datetime.datetime.now()
        filename = f"qrcode_{now.strftime('%Y%m%d_%H%M%S')}.png"
        img.save(filename)


def qrcode_styled_generator(size: int, text: Optional[str] = None, url: Optional[str] = None, contact: Optional[str] = None, color: Optional[str] = None, path: Optional[str] = None, style: str = "rounded") -> None:
    """
    Генерирует стилизованный QR-код.
    """
    if not any([text, url, contact]):
        raise ValueError("Необходимо указать один из аргументов: text, url, contact.")
    if sum([bool(text), bool(url), bool(contact)]) > 1:
        raise ValueError("Можно указать только один из аргументов: text, url, contact.")

    data = text or url or contact

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Цвета
    if color:
        try:
            background_color, qr_color = map(str.strip, color.split(","))
        except ValueError:
            background_color, qr_color = "#ffffff", "#000000"  # Default if parsing fails
    else:
        background_color, qr_color = "#ffffff", "#000000"  # Default colors

    # Стили
    if style == "rounded":
        img = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer()) #  Удалите , color_mask=SquareRootColorMask(back_color=background_color, front_color=qr_color) если у вас старая версия qrcode
    else:  # "square"
        img = qr.make_image(fill_color=qr_color, back_color=background_color) # Square modules

    # Размер
    img = img.resize((size, size))

    # Сохранение
    if path:
        img.save(path)
    else:
        # Default filename
        now = datetime.datetime.now()
        filename = f"qrcode_{now.strftime('%Y%m%d_%H%M%S')}.png"
        img.save(filename)


def qrcode(size: int, text: Optional[str] = None, url: Optional[str] = None, contact: Optional[str] = None, color: Optional[str] = None, path: Optional[str] = None, styled: bool = False) -> None:
    """
    Генерирует QR-код (обычный или стилизованный).
    """
    if styled:
        qrcode_styled_generator(size=size, text=text, url=url, contact=contact, color=color, path=path)
    else:
        qrcode_generator(size=size, text=text, url=url, contact=contact, color=color, path=path)