# code for bbc news screen
import qrcode
from kivy.properties import StringProperty
from kivy.uix import label, image
from kivy.uix.screenmanager import Screen

from apis.news_bbc import get_headlines_bbc_news


class BBCNewsScreen(Screen):
    newsRegion = StringProperty("uk")  # Default to UK news
    articleTitle = StringProperty()
    articleDescription = StringProperty()
    articleURL = StringProperty()

    print("mrow", newsRegion, "mrow")

    if newsRegion not in ["", "uk", "usa", "world"]:
        raise ValueError("Invalid region. Currently, only 'uk', 'usa', or 'world' is accepted.")

    try:
        # create qrcode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=0,
        )
        qr.add_data(articleURL)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        if newsRegion == "uk":
            BBCNewsSlogan = "BBC News - UK"
        elif newsRegion == "usa":
            BBCNewsSlogan = "BBC News - USA"
        elif newsRegion == "world":
            BBCNewsSlogan = "BBC News - World"
        else:
            raise ValueError("Invalid region. Currently, only 'uk', 'usa', or 'world' is accepted.")

        BBCNewsLocationLabel =           label.Label(text=BBCNewsSlogan,      font_name="assets/fonts/bbcfont/BBCReithSans_A_BoldItalic.ttf",    font_size=24)
        BBCNewsArticleTitleLabel =       label.Label(text=articleTitle,       font_name="assets/fonts/bbcfont/BBCReithSans_A_Bold.ttf",          font_size=18)
        BBCNewsArticleDescriptionLabel = label.Label(text=articleDescription, font_name="assets/fonts/bbcfont/BBCReithSans_A_RegularItalic.ttf", font_size=14)

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
        draw.text((8, 10), BBCNewsSlogan, font=bbc_uk_news_slogan_font, fill="black")

        if len(artitleTitle) >= 90:  # if the title is longer than 90 characters
            artitleTitle = artitleTitle[:90] + "..."  # Truncate the title and add ellipsis

        draw.text((10, 40), wrap_text(artitleTitle, bbc_article_title_font, 360, draw), font=bbc_article_title_font, fill="black")

        # If the description is too long, wrap it
        articleDescription = articleDescription.replace("\n", " ")  # Replace newlines with spaces for better formatting
        if len(articleDescription) > 300:  # If the description is longer than 300 characters
            articleDescription = articleDescription[:300] + "..."  # Truncate the description and add ellipsis

        draw.text((6, 80), wrap_text(articleDescription, bbc_content_font, 306, draw), font=bbc_content_font, fill="black")

        # Draw a black line below where the logo and title is
        draw.line([0, 32, width / 3 * 2, 32], fill="black", width=2)

        # draw another black line just below the article title for styling and separation
        draw.line([5, 72, width / 10 * 2, 72], fill="black", width=2)




    except Exception as e:
        raise e.with_traceback(e.__traceback__)
