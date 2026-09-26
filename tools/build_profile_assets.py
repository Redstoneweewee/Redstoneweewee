"""Build the profile header and compact portfolio preview from local assets."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FONT_DIR = Path("C:/Windows/Fonts")


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), size)


def rounded_image(source: Image.Image, size: int) -> Image.Image:
    photo = source.convert("RGB").resize((size, size), Image.Resampling.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    output = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    output.paste(photo, (0, 0), mask)
    return output


def build_header() -> None:
    width, height = 1200, 340
    canvas = Image.new("RGBA", (width, height), "#0d1117")
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((785, -210, 1440, 470), fill=(31, 111, 235, 62))
    gd.ellipse((-180, 150, 380, 640), fill=(45, 91, 165, 24))
    canvas = Image.alpha_composite(canvas, glow.filter(ImageFilter.GaussianBlur(70)))
    d = ImageDraw.Draw(canvas)

    for x in range(0, width, 48):
        d.line((x, 0, x, height), fill="#192638", width=1)
    for y in range(0, height, 48):
        d.line((0, y, width, y), fill="#192638", width=1)

    d.rounded_rectangle((1, 1, width - 2, height - 2), radius=18, outline="#303b4b", width=2)
    d.rounded_rectangle((58, 41, 64, 300), radius=3, fill="#58a6ff")

    small = font("segoeuib.ttf", 19)
    title = font("segoeuib.ttf", 76)
    subtitle = font("segoeui.ttf", 27)
    chip_font = font("segoeuib.ttf", 17)

    d.text((88, 43), "ENGINEER  /  DESIGNER  /  CREATOR", font=small, fill="#8fbff7")
    d.text((83, 82), "Leifeng Chen", font=title, fill="#f0f6fc", stroke_width=0)
    d.text((88, 186), "I design things people use, then watch where they get stuck.", font=subtitle, fill="#b9c8d8")

    chips = [
        (88, 258, 335, "3.5M+  DOWNLOADS"),
        (349, 258, 565, "64K+  SUBSCRIBERS"),
        (579, 258, 773, "307  GAME TESTS"),
    ]
    for left, top, right, label in chips:
        d.rounded_rectangle((left, top, right, top + 40), radius=20, fill="#1b283a", outline="#3b5676", width=1)
        d.text((left + 15, top + 9), label, font=chip_font, fill="#dbeaff")

    photo_size = 174
    photo_x, photo_y = 954, 78
    d.ellipse((photo_x - 12, photo_y - 12, photo_x + photo_size + 12, photo_y + photo_size + 12), outline="#4d84bd", width=2)
    d.ellipse((photo_x - 24, photo_y - 24, photo_x + photo_size + 24, photo_y + photo_size + 24), outline="#263f5a", width=1)
    avatar = rounded_image(Image.open(ASSETS / "avatar.webp"), photo_size)
    canvas.alpha_composite(avatar, (photo_x, photo_y))

    for x, y, s in [(1115, 38, 12), (1136, 38, 12), (1115, 59, 12), (1136, 59, 12), (1094, 59, 12)]:
        d.rounded_rectangle((x, y, x + s, y + s), radius=2, fill="#3a68a1")

    canvas.convert("RGB").save(ASSETS / "profile-header.png", optimize=True)


def build_site_card() -> None:
    source = Image.open(ASSETS / "site-preview.png").convert("RGB")
    crop = source.crop((0, 0, source.width, min(650, source.height)))
    card_width = 1080
    card_height = round(crop.height * card_width / crop.width)
    crop = crop.resize((card_width, card_height), Image.Resampling.LANCZOS)
    mask = Image.new("L", crop.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, card_width - 1, card_height - 1), radius=14, fill=255)
    card = Image.new("RGBA", crop.size, (0, 0, 0, 0))
    card.paste(crop, (0, 0), mask)
    d = ImageDraw.Draw(card)
    d.rounded_rectangle((0, 0, card_width - 1, card_height - 1), radius=14, outline="#386eaa", width=3)
    card.save(ASSETS / "site-card.png", optimize=True)


if __name__ == "__main__":
    build_header()
    build_site_card()
