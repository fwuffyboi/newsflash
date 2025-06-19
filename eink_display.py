# This file is for displaying messages on the (presumably) attached E-Ink display.
import time
from PIL import Image, ImageDraw, ImageFont
# from waveshare_epd import epd3in5g, epdconfig todo


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
        raise ValueError("Invalid status. Must be 'fatal', 'warning', or 'info'.")

    # Load the font
    try:
        font = ImageFont.truetype("NotoSansFont/static/NotoSans-SemiBoldItalic.ttf", 20)
        message_font = ImageFont.truetype("NotoSansFont/static/NotoSans-Light.ttf", 14)
        timeout_font = ImageFont.truetype("NotoSansFont/static/NotoSans-Medium.ttf", 8)
    except IOError:
        font = ImageFont.load_default()


    # Create a blank image for drawing
    width, height = 384, 184  # Screen resolution for my particular E-Ink display
    # Create a new image with white background
    image = Image.new("RGB", (width, height), "white")  # White background
    draw = ImageDraw.Draw(image)

    # Draw a corresponding background based on the status
    if status == "fatal":
        # use a red background
        draw.rectangle([0, 0, width, height], fill="red")

        # draw an information icon to the left
        draw.ellipse([10, 10, 49, 49], fill="black")  # Black circle for info icon
        draw.ellipse([13, 13, 46, 46], fill="red")
        exclamation_font = ImageFont.truetype("NotoSansFont/static/NotoSans-Medium.ttf", 30)
        draw.text(xy=(26, 7), text="!", font=exclamation_font, fill="black")

    elif status == "warn":
        # yellow background
        draw.rectangle([0, 0, width, height], fill="yellow")

        # Draw a triangle (warning icon)
        draw.polygon([10, 49, 30, 10, 50, 49], fill="yellow", width=3, outline="black")

        # draw the exclamation mark inside the triangle
        exclamation_font = ImageFont.truetype("NotoSansFont/static/NotoSans-Medium.ttf", 30)
        draw.text(xy=(26, 11), text="!", font=exclamation_font, fill="black")


    elif status == "info":
        # no need for a background since its alr white

        # draw an information icon to the left
        draw.ellipse([10, 10, 49, 49], fill="black")  # Black circle for info icon
        draw.ellipse([13, 13, 46, 46], fill="white")
        exclamation_font = ImageFont.truetype("NotoSansFont/static/NotoSans-Medium.ttf", 30)
        draw.text(xy=(26, 7), text="!", font=exclamation_font, fill="black")

    else:
        raise ValueError("Invalid status. Must be 'fatal', 'warning', or 'info'.")

    # Draw the title and message
    if status == "fatal":
        title = "Критическая ошибка!!"  # Critical Error!
    elif status == "warn":
        title = "Внимание!"  # Attention!
    elif status == "info":
        title = "Информация"  # Information
    else:
        title = "how did you get here?"  # This should never happen

    # Draw a black line below where the icons and text is
    draw.line([0, 60, width / 3 * 2, 60], fill="black", width=2)

    # Detect if the message is too long and needs to be wrapped. It will avoid wrapping inside of words too.
    if len(message) > 100:

        # is it TOO long?
        if len(message) > 330:
            raise ValueError("Message is too long. Please shorten it to less than 350 characters.")

        wrapped_message = ""
        line_length = 0

        for word in message.split():
            for letter in word:
                if letter == "\n":
                    wrapped_message += "\n"
                    line_length = 0
                else:
                    wrapped_message += letter
                    line_length += 1
            wrapped_message += " "  # add a space after each word


            if line_length + len(word) > 50:
                wrapped_message += "\n"
                line_length = 0  # reset line length after wrapping

        message = wrapped_message

    # Draw the title and message on the image
    draw.text((60, 15), title, font=font, fill=0)  # write title in black text
    draw.text((10, 70), message, font=message_font, fill=0)  # write message in black text

    # show the timeout and time on the bottom right corner
    current_time = time.strftime("%H:%M:%S", time.localtime())
    draw.text((width - 60, height - 20), f"Timeout: {timeout}s", font=timeout_font, fill=0)  # Timeout text
    draw.text((width - 60, height - 10), f"Time: {current_time}", font=timeout_font, fill=0)  # Current time text

    print(len(message))

    # Save the image to a file todo
    image_path = "eink_display_message.png" # todo
    image.save(image_path) # todo

    # Display the image on the E-Ink display
    # clear_display()               # first clear the display todo
    # display_image(image, timeout) # then display the image todo


def display_image(image, timeout=3):
    """
    Displays an image on the E-Ink display.

    :param image: File to display.
    :param timeout: Time in seconds to display the image before clearing the screen. Default is 3. Use -1 for indefinite display.
    """

    clear_display() # first, clear the display in case it was not cleared before

    epd = epd3in5g.EPD()              # create an instance of the EPD class
    epd.init()                        # initialize the display
    epd.display(epd.getbuffer(image)) # display the image given
    epd.sleep()                       # display go sleepy sleep for power saving

    # wait for timeout
    if timeout == -1:
        # wait indefinitely
        while True:
            time.sleep(1)

    # clear the display
    epd.Clear() # clear the display
    epd.sleep() # go sleepy sleep for even more power saving
    epdconfig.RaspberryPi.module_exit(cleanup=True)  # exit and clean up


def clear_display():
    """
    Clears the E-Ink display.
    """
    epd = epd3in5g.EPD()  # create an instance of the EPD class
    epd.init()  # initialize the display
    epd.Clear()  # clear the display
    epd.sleep()  # put to sleep so it doesn't break the display
    epdconfig.RaspberryPi.module_exit(cleanup=True)  # exit and clean up
