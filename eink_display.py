# This file is for displaying messages on the (presumably) attached E-Ink display.
import time

from PIL import Image, ImageDraw, ImageFont

from assets.pillow_wraptext import wrap_text
from waveshare_epd import epd3in5g


def show_message(status, message, timeout=3):
    """
    Displays a message on the E-Ink display.
    Note: The E-Ink display supports only black, white, and yellow colors.

    :param status: "fatal", "warning", or "info"
    :param message: The message to display
    :param timeout: Time in seconds to display the message before clearing the screen. Default is 3. Not required.
    """

    # Check if the status is valid
    if status not in ["fatal", "warn", "info"]:
        raise ValueError("Invalid status. Must be 'fatal', 'warn', or 'info'.")

    # Load the font
    font = ImageFont.truetype("assets/fonts/NotoSansFont/static/NotoSans-SemiBoldItalic.ttf", 24)
    message_font = ImageFont.truetype("assets/fonts/NotoSansFont/static/NotoSans-Light.ttf", 15)
    timeout_font = ImageFont.truetype("assets/fonts/NotoSansFont/static/NotoSans-MediumItalic.ttf", 10)

    # Create a blank image for drawing
    width, height = 384, 184  # Screen resolution for my particular E-Ink display
    # Create a new image with white background
    image = Image.new("RGB", (width, height), "white")  # White background
    draw = ImageDraw.Draw(image)

    # Draw a corresponding background based on the status
    if status == "fatal":
        # use a red background
        draw.rectangle([0, 0, width, height], fill="red")

        # draw a stop sign icon to the left

        # top and bottom lines
        draw.line([(20, 10), (40, 10)], width=3, fill="white")  # t
        draw.line([(20, 50), (40, 50)], width=3, fill="white")  # b
        # left and right lines
        draw.line([(10, 20), (10, 40)], width=3, fill="white")  # l
        draw.line([(50, 20), (50, 40)], width=3, fill="white")  # r
        # diagonal lines                                       #todo/keep?
        draw.line([(10, 10), (50, 50)], width=3, fill="white")  # todo/keep?
        draw.line([(10, 50), (50, 10)], width=3, fill="white")  # todo/keep?
        # corner lines
        draw.line([(40, 10), (50, 20)], width=3, fill="white")  # tr
        draw.line([(20, 10), (10, 20)], width=3, fill="white")  # tl
        draw.line([(10, 40), (20, 50)], width=3, fill="white")  # bl
        draw.line([(40, 50), (50, 40)], width=3, fill="white")  # br

        # draw the "STOP" text inside the stop sign icon
        exclamation_font = ImageFont.truetype("assets/fonts/NotoSansFont/static/NotoSans-Medium.ttf", 14)
        draw.text(xy=(13, 20), text="STOP", font=exclamation_font, fill="white")

    elif status == "warn":
        # yellow background
        draw.rectangle([0, 0, width, height], fill="yellow")

        # Draw a triangle (warning icon)
        draw.polygon([10, 49, 30, 10, 50, 49], fill="yellow", width=3, outline="black")

        # draw the exclamation mark inside the triangle
        exclamation_font = ImageFont.truetype("assets/fonts/NotoSansFont/static/NotoSans-Medium.ttf", 30)
        draw.text(xy=(26, 11), text="!", font=exclamation_font, fill="black")

    elif status == "info":
        # no need for a background since its already white

        # draw an information icon to the left
        draw.ellipse([10, 10, 49, 49], fill="black")  # Black circle for info icon
        draw.ellipse([13, 13, 46, 46], fill="white")
        exclamation_font = ImageFont.truetype("assets/fonts/NotoSansFont/static/NotoSans-Medium.ttf", 30)
        draw.text(xy=(26, 7), text="!", font=exclamation_font, fill="black")

    else:
        raise ValueError("Invalid status. Must be 'fatal', 'warning', or 'info'.")

    # Draw the title and message
    if status == "fatal":
        title = "Критическая ошибка!!"  # Critical Error!
    elif status == "warn":
        title = "Внимание!"  # Attention!
    elif status == "info":
        title = "Информация!"  # Information
    else:
        title = "как..? (" + status + ").."  # This should never happen

    # Draw a line below where the icons and text is
    if status == "fatal":
        draw.line([0, 60, width / 3 * 2, 60], fill="white", width=2)
    else:
        draw.line([0, 60, width / 3 * 2, 60], fill="black", width=2)

    # Draw the title and message on the image
    if status == "fatal":
        draw.text((60, 15), title, font=font, fill="white")  # more visible in white on red background
        draw.text((10, 70), wrap_text(message, message_font, 360, draw), font=message_font, width=2, fill="white")
    else:
        draw.text((60, 15), title, font=font, fill="black")  # write title in black text
        draw.text((10, 70), wrap_text(message, message_font, 360, draw), font=message_font, fill="black")  # write message in black text

    # show the timeout and time just above the line
    current_time = time.strftime("%H:%M:%S", time.localtime())
    if status == "fatal":
        draw.text((110, 46), f"t,ac: {current_time}, gmt+{time.timezone}, t.o.: {timeout}", font=timeout_font,
                  fill="white")
    else:
        draw.text((110, 46), f"t,ac: {current_time}, gmt+{time.timezone}, t.o.: {timeout}", font=timeout_font,
                  fill="black")

    # Save the image to a file todo/debug
    # image_path = "eink_display_message.png"  # todo/debug
    # image.save(image_path)  # todo/debug

    # Display the image on the E-Ink display
    display_image(image, timeout)  # then display the image


def display_image(image, timeout=3):
    """
    Displays an image on the E-Ink display.

    :param image: File to display.
    :param timeout: Time in seconds to display the image before clearing the screen. Default is 3. Use -1 for indefinite display.
    """

    epd = epd3in5g.EPD()  # create an instance of the EPD class
    epd.init()  # initialize the display
    epd.display(epd.getbuffer(image))  # display the image given
    epd.sleep()  # display go sleepy sleep

    # wait for timeout
    if timeout == -1:
        # wait indefinitely
        while True:
            time.sleep(1)
    else:
        # wait for the specified timeout
        time.sleep(timeout)


def clear_display(mode="easy"):
    """
    Clears the E-Ink display.
    """
    if mode not in ["easy", "full"]:
        raise ValueError("Invalid mode. Must be 'easy' or 'full'.")

    if mode == "easy":
        # easy mode: just put white and black, then white on the display
        epd = epd3in5g.EPD()
        epd.init()

        imwhite = Image.new("1", (epd.width, epd.height), 255)
        imblack = Image.new("1", (epd.width, epd.height), 0)

        for _ in range(5):
            epd.display(epd.getbuffer(imwhite))
            epd.display(epd.getbuffer(imblack))

        epd.display(epd.getbuffer(imwhite))  # display white on the screen
        epd.sleep()  # put to sleep so it doesn't break the display


    elif mode == "full":
        epd = epd3in5g.EPD()  # create an instance of the EPD class
        epd.init()  # initialize the display
        epd.Clear()  # clear the display
        epd.sleep()  # put to sleep so it doesn't break the display
