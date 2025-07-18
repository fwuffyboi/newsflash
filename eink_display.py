# This file is for displaying messages on the (presumably) attached E-Ink display.
import time


def display_image(image, timeout=3):
    """
    Displays an image on the E-Ink display.

    :param image: File to display.
    :param timeout: Time in seconds to display the image before clearing the screen. Default is 3. Use -1 for indefinite display.
    """

    print(f"displaying...")


def clear_display():
    """
    Clears the E-Ink display.
    """
    epd = epd3in5g.EPD()  # create an instance of the EPD class
    epd.init()  # initialize the display
    epd.Clear()  # clear the display
    epd.sleep()  # put to sleep so it doesn't break the display
