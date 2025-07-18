# code for the time and date screen of the E-Ink display
from assets.pillow_wraptext import wrap_text


def current_weather_screen(timeout: int = 10, current_weather_conditions: str = "Unknown",
                           current_temperature_celsius: float = 00000, UV_index: int = 00000,
                           current_humidity_percentage: int = 000,
                           users_name: str = "doerrornowmrow:33"):
    """
    Displays the current time and date on screen. Also says the current weather condition and temperature.
    """

    import time
    from eink_display import display_image
    from screens.message import show_message
    from PIL import Image, ImageDraw, ImageFont, ImageOps
    import qrcode

    try:
        if users_name == "doerrornowmrow:33" or not users_name: # this is definitely not somebody's name, so raise an error
            raise ValueError("users_name must be set to a valid name! (This is caused by not sending a name to the function).")

        # basic silly shit to make the image
        width, height = 384, 184  # Screen resolution for my particular E-Ink display # todo/unify
        image = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(image)

        title_font    = ImageFont.truetype("assets/fonts/NotoSansFont/static/NotoSans-BoldItalic.ttf", 24)
        content_font  = ImageFont.truetype("assets/fonts/NotoSansFont/static/NotoSans-MediumItalic.ttf", 16)
        info_font     = ImageFont.truetype("assets/fonts/NotoSansFont/static/NotoSans-Regular.ttf", 13)
        tiny_font     = ImageFont.truetype("assets/fonts/NotoSansFont/static/NotoSans-MediumItalic.ttf", 11)
        degrees_font  = ImageFont.truetype("assets/fonts/NotoSansFont/static/NotoSans-Black.ttf", 40)
        humidity_font = ImageFont.truetype("assets/fonts/NotoSansFont/static/NotoSans-Black.ttf", 30)
        uv_font       = ImageFont.truetype("assets/fonts/UVFont/WDXLLubrifontSC-Regular.ttf", 65)

        # make background white
        draw.rectangle([0, 0, width, height], fill="white")

        # Make qr code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=0,
        )
        qr.add_data("https://weather.metoffice.gov.uk/maps-and-charts/uk-weather-map")
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # draw the QR code in the bottom right corner
        qr_img = qr_img.resize((64, 64))  # Resize the QR code to fit the screen
        image.paste(qr_img, (width - 68, height - 68))  # Paste the QR code in the top right corner

        # Draw the title
        draw.text((6, 3), "Current weather", font=title_font, fill="black")

        # Add google weather logo
        google_logo = Image.open("assets/GoogleWeather.png")
        google_logo = google_logo.resize((55, 55))  # Resize the logo to fit the screen
        image.paste(google_logo, (width - 50, -5), google_logo)  # Paste the logo in the top right corner, making sure to use a mask

        # Draw current temperature
        if current_temperature_celsius == 00000: # if temperature is unknown, say "??.?" instead
            current_temperature_celsius = "??.!"
        draw.text((4, 118), f"{current_temperature_celsius}°c", font=degrees_font, fill="black")

        # Draw current humidity
        if current_humidity_percentage == 000:
            current_humidity_percentage = "??!"
        draw.text((150, 128), f"{current_humidity_percentage}%", font=humidity_font, fill="black")

        # Draw weather condition as text
        if current_weather_conditions == "Unknown":
            current_weather_conditions = "Unknown conditions - ??!"
        draw.text((6, 162), f"{current_weather_conditions}", font=content_font, fill="black")

        # Draw a black line below the title
        draw.line([0, 32, width / 3 * 2, 32], fill="black", width=2)

        # Draw another black line just above the weather condition text
        draw.line([4, 163, width / 10 * 6, 163], fill="black", width=2)

        # Draw text on top of the QR code
        draw.text((315, 88),  "Scan for M.O.", font=tiny_font, fill="black")
        draw.text((315, 100), "weather map",   font=tiny_font, fill="black")

        # Draw UV index if provided
        if UV_index != 00000:

            if UV_index != 0: # if UV index is not 0, draw the UV index icon
                # Draw a left angled triangle as a warning icon
                draw.polygon([260, height-4, 310, height-68, 310, height-4], fill="yellow", width=5, outline="yellow")

                # draw the uv number inside the triangle thing
                if UV_index in [10, 12]:  # if UV index is a physically big number (as in space, not numerical value)
                    # 11 doesnt count cus it works fine so fuck you
                    draw.text(xy=(262, height-70), text=f"{UV_index}", font=uv_font, fill="black") # move it left slightly so it doesn't fuck the qr code up
                elif UV_index == 1:
                    # move it slightly to the right to make it look better
                    draw.text(xy=(285, height-70), text=f"{UV_index}", font=uv_font, fill="black")
                else:
                    draw.text(xy=(275, height-70), text=f"{UV_index}", font=uv_font, fill="black") # normal

            # Write a greeting/description thing of the current conditions based on multiple values
            description = ["Good "]

            # figure out if its morning, afternoon, evening or night
            current_hour = time.localtime().tm_hour
            if 4 <= current_hour < 12: # all of 4am-11am
                description.append("morning")
            elif 12 <= current_hour < 18: # all of 12pm-5pm
                description.append("afternoon")
            elif 18 <= current_hour < 21: # all of 6pm-8pm
                description.append("evening")
            else: # all of 9pm-3am
                description.append("night")

            description.append(f", {users_name}!\n")
            if current_weather_conditions.lower() != "Unknown" or current_temperature_celsius != 00000: # if both are good!
                description.append(f"Currently, it is {current_weather_conditions.lower()}, and the temperature is {current_temperature_celsius}°c")
            elif current_temperature_celsius == 00000: # if temperature is unknown...
                description.append(f"Current temperature is unknown.")
            elif current_weather_conditions == "Unknown": # if weather conditions are unknown...
                description.append(f"Current weather conditions are unknown.")

            if 1 <= UV_index <= 2: # if UV index is equal to or more than 1/less than or equal to 2
                description.append(f" With a UV index of {UV_index}.")
            elif UV_index >= 3:  # if UV index is more than or equal to 3
                # check the time, if it is between 4 and 15, say "Check the UV index before going outside today!"
                if 4 <= current_hour <= 15: # if it is between 0400 and 1500
                    description.append(f" With a UV index of {UV_index}! Check the UV index if going outside today or later!")
                else:  # if it is not between 0400 and 1500
                    description.append(f" With a UV index of {UV_index}! Precautions recommended if going outside soon!")

            if current_humidity_percentage != 000:  # if humidity is known
                if current_humidity_percentage < 30: # if humidity is less than 30%
                    description.append(f" The air seems quite dry ({current_humidity_percentage}%).")
                elif 30 <= current_humidity_percentage <= 60: # if humidity is between 30% and 60%
                    description.append(f" The air should be comfortable ({current_humidity_percentage}%).")
                else: # if humidity is more than 60%
                    description.append(f" The air should feel quite humid ({current_humidity_percentage}%).")
            else:  # if humidity is unknown
                description.append(" The humidity is currently unknown (??!%).")

            # write the description text on the screen
            draw.text((6, 36), wrap_text(text="".join(description), font=info_font, draw=draw, max_width=306), font=info_font, fill="black")

        # Show the message on the E-Ink display
        display_image(image, timeout)


    except Exception as e:
        show_message(status="fatal", message=f"Error displaying current_weather_screen!: {str(e)}", timeout=-1)
        raise e.with_traceback(e.__traceback__)
