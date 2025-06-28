# code for bbc news screen
from assets.pillow_wraptext import wrap_text
from eink_display import display_image


def bbc_news_screen(region: str, articleTitle: str, articleDesc: str, articleLink: str, timeout: int = 10):
    """
    Displays the given variables as UK headlines from BBC News.
    """
    from eink_display import show_message
    from PIL import Image, ImageDraw, ImageFont
    import qrcode

    if region not in ["UK", "USA", "WORLD"]:
        raise ValueError("Invalid region. Currently, only 'UK', 'USA', or 'WORLD' is accepted.")

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

        # Draw the bbc news region
        draw.text((8, 10), bbc_news_slogan, font=bbc_uk_news_slogan_font, fill="black")

        if len(title) >= 90:  # if the title is longer than 90 characters
            title = title[:90] + "..."  # Truncate the title and add ellipsis

        draw.text((10, 40), wrap_text(title, bbc_article_title_font, 360, draw), font=bbc_article_title_font, fill="black")

        # If the description is too long, wrap it
        desc = desc.replace("\n", " ")  # Replace newlines with spaces for better formatting
        if len(desc) > 300:  # If the description is longer than 300 characters
            desc = desc[:300] + "..."  # Truncate the description and add ellipsis

        draw.text((6, 80), wrap_text(desc, bbc_content_font, 360, draw), font=bbc_content_font, fill="black")

        # Draw a black line below where the logo and title is
        draw.line([0, 32, width / 3 * 2, 32], fill="black", width=2)

        # Draw a black line just above the description text
        draw.line([5, 72, width / 10 * 2, 72], fill="black", width=2)

        # Show the message on the E-Ink display
        display_image(image, timeout)


    except Exception as e:
        show_message(status="fatal", message=f"Error fetching BBC News: {str(e)}", timeout=5)
        raise e
