from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import requests
import math
import os

class Generator:
    def __init__(self):
        self.default_bg = os.path.join(os.path.dirname(__file__), 'assets', 'card.png')
        self.online     = os.path.join(os.path.dirname(__file__), 'assets', 'online.png')
        self.offline    = os.path.join(os.path.dirname(__file__), 'assets', 'offline.png')
        self.idle       = os.path.join(os.path.dirname(__file__), 'assets', 'idle.png')
        self.dnd        = os.path.join(os.path.dirname(__file__), 'assets', 'dnd.png')
        self.streaming  = os.path.join(os.path.dirname(__file__), 'assets', 'streaming.png')
        self.font1      = os.path.join(os.path.dirname(__file__), 'assets', 'font.ttf')
        self.font2      = os.path.join(os.path.dirname(__file__), 'assets', 'font2.ttf')

    def generate_profile(self, bg_image:str=None, profile_image:str=None, level:int=1, current_xp:int=0, user_xp:int=20, next_xp:int=100, user_position:int=1, user_name:str='Shahriyar#9770', user_status:str='online'):
        if not bg_image:
            card = Image.open(self.default_bg).convert("RGBA")
        else:
            bg_bytes = BytesIO(requests.get(bg_image).content)
            card = Image.open(bg_bytes).convert("RGBA")

            width, height = card.size
            if width == 900 and height == 238:
                pass
            else:
                x1 = 0
                y1 = 0
                x2 = width
                nh = math.ceil(width * 0.264444)
                y2 = 0

                if nh < height:
                    y1 = (height / 2) - 119
                    y2 = nh + y1

                card = card.crop((x1, y1, x2, y2)).resize((900, 238))

        profile_bytes = BytesIO(requests.get(profile_image).content)
        profile = Image.open(profile_bytes)
        profile = profile.convert('RGBA').resize((180, 180))

        if user_status == 'online':
            status = Image.open(self.online)
        if user_status == 'offline':
            status = Image.open(self.offline)
        if user_status == 'idle':
            status = Image.open(self.idle)
        if user_status == 'streaming':
            status = Image.open(self.streaming)
        if user_status == 'dnd':
            status = Image.open(self.dnd)

        status = status.convert("RGBA").resize((40,40))

        profile_pic_holder = Image.new(
            "RGBA", card.size, (255, 255, 255, 0)
        )  # Is used for a blank image so that i can mask

        # Mask to crop image
        mask = Image.new("RGBA", card.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse(
            (29, 29, 209, 209), fill=(255, 25, 255, 255)
        )  # The part need to be cropped

        # Editing stuff here

        # ======== Fonts to use =============
        font_normal = ImageFont.truetype(self.font1, 36)
        font_small = ImageFont.truetype(self.font1, 20)
        font_signa = ImageFont.truetype(self.font2, 25)

        # ======== Colors ========================
        WHITE = (189, 195, 199)
        DARK = (110 151 241)
        YELLOW = (255, 234, 167)

        def get_str(xp):
            if xp < 1000:
                return str(xp)
            if xp >= 1000 and xp < 1000000:
                return str(round(xp / 1000, 1)) + "k"
            if xp > 1000000:
                return str(round(xp / 1000000, 1)) + "M"

        draw = ImageDraw.Draw(card)
        draw.text((245, 22), user_name, DARK, font=font_normal)
        draw.text((245, 98), f"Rank #{user_position}", DARK, font=font_small)
        draw.text((245, 123), f"Level {level}", DARK, font=font_small)
        draw.text(
            (245, 150),
            f"Exp {get_str(user_xp)}/{get_str(next_xp)}",
            DARK,
            font=font_small,
        )

        # Adding another blank layer for the progress bar
        # Because drawing on card dont make their background transparent
        blank = Image.new("RGBA", card.size, (255, 255, 255, 0))
        blank_draw = ImageDraw.Draw(blank)
        blank_draw.rectangle(
            (245, 185, 750, 205), fill=(255, 255, 255, 0), outline=DARK
        )

        xpneed = next_xp - current_xp
        xphave = user_xp - current_xp

        current_percentage = (xphave / xpneed) * 100
        length_of_bar = (current_percentage * 4.9) + 248

        blank_draw.rectangle((248, 188, length_of_bar, 202), fill=DARK)
        blank_draw.ellipse((20, 20, 218, 218), fill=(255, 255, 255, 0), outline=DARK)

        profile_pic_holder.paste(profile, (29, 29, 209, 209))

        pre = Image.composite(profile_pic_holder, card, mask)
        pre = Image.alpha_composite(pre, blank)

        # Status badge
        # Another blank
        blank = Image.new("RGBA", pre.size, (255, 255, 255, 0))
        blank.paste(status, (169, 169))

        final = Image.alpha_composite(pre, blank)
        final_bytes = BytesIO()
        final.save(final_bytes, 'png')
        final_bytes.seek(0)
        return final_bytes
