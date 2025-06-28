# code for bbc news screen

from eink_display import display_image


def time_and_date_world(region: str, articleTitle: str, articleDesc: str, articleLink: str, timeout: int = 10):
    """
    Displays the current time and date on screen. With slight calendar and weather information.
    """
    from eink_display import show_message
    from PIL import Image, ImageDraw, ImageFont
    import qrcode


    try:
        title = articleTitle
        desc = articleDesc

        # create qrcode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=0,
        )
        qr.add_data(articleLink)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # basic silly shit to make the image
        width, height = 384, 184  # Screen resolution for my particular E-Ink display # todo/unify
        image = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(image)

        if region.lower() == "uk":
            bbc_news_slogan = "BBC News - UK"
        elif region.lower() == "usa":
            bbc_news_slogan = "BBC News - USA"
        elif region.lower() == "world":
            bbc_news_slogan = "BBC News - World"

        bbc_uk_news_slogan_font = ImageFont.truetype("assets/fonts/bbcfont/BBCReithSans_A_Bold.ttf", 24)
        bbc_article_title_font = ImageFont.truetype("assets/fonts/bbcfont/BBCReithSans_A_Bold.ttf", 14)
        bbc_content_font = ImageFont.truetype("assets/fonts/bbcfont/BBCReithSans_A_RegularItalic.ttf", 12)

        # make background white
        draw.rectangle([0, 0, width, height], fill="white")

        # draw BBC logo in top left corner
        bbc_logo = Image.open("assets/BBC-logo.png")  # Ensure you have the BBC logo image in the assets folder
        bbc_logo = bbc_logo.resize((120, 100))  # Resize the logo to fit the screen
        draw.bitmap((280, -30), bbc_logo, fill="black")  # Draw the logo on the image

        # draw the QR code in the bottom right corner
        qr_img = qr_img.resize((64, 64))  # Resize the QR code to fit the screen
        image.paste(qr_img, (width - 68, height - 68))  # Paste the QR code in the top right corner

        # Draw the bbc news title
        draw.text((8, 10), bbc_news_slogan, font=bbc_uk_news_slogan_font, fill="black")

        # Draw the title text, on two lines if necessary
        DESC_ONE_LINE_LOWER = False

        print("lentitle:", len(title))  # todo/debug

        draw.text((10, 40), title, font=bbc_article_title_font, fill="black")

        # Draw the content text, but make sure it fits within the screen width with a text box
        desc = desc.replace("\n", " ")  # Replace newlines with spaces for better formatting

        draw.text((6, 80), desc, font=bbc_content_font, fill="black")

        # Draw a black line below where the logo and title is
        draw.line([0, 32, width / 3 * 2, 32], fill="black", width=2)

        # Draw a black line just above the description text
        draw.line([5, 72, width / 10 * 2, 72], fill="black", width=2)

        # Show the message on the E-Ink display
        display_image(image, timeout)


    except Exception as e:
        show_message(status="fatal", message=f"Error fetching BBC News: {str(e)}", timeout=5)
        raise e
