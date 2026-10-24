from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "IMAGES" / "logo.jpg"
OUTPUT_SIZE = 1024
LANCZOS = Image.Resampling.LANCZOS


def make_icon() -> Image.Image:
    logo = Image.open(SOURCE).convert("RGB")
    width, height = logo.size
    logo = logo.crop((5, 5, width - 5, height - 5))

    canvas = Image.new("RGB", (784, 784), "white")
    offset = ((784 - logo.width) // 2, (784 - logo.height) // 2)
    canvas.paste(logo, offset)
    canvas = canvas.resize((OUTPUT_SIZE, OUTPUT_SIZE), LANCZOS).convert("RGBA")

    draw = ImageDraw.Draw(canvas)
    draw.ellipse((6, 6, 1017, 1017), outline="#F15A0A", width=12)

    mask = Image.new("L", (OUTPUT_SIZE, OUTPUT_SIZE), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, OUTPUT_SIZE - 1, OUTPUT_SIZE - 1), fill=255)
    canvas.putalpha(mask)
    return canvas


def main() -> None:
    icon = make_icon()
    icon.resize((32, 32), LANCZOS).save(ROOT / "favicon-32.png")
    icon.resize((192, 192), LANCZOS).save(ROOT / "favicon-192.png")
    icon.save(ROOT / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])

    apple = Image.new("RGB", (180, 180), "white").convert("RGBA")
    apple_icon = icon.resize((156, 156), LANCZOS)
    apple.alpha_composite(apple_icon, (12, 12))
    apple.convert("RGB").save(ROOT / "apple-touch-icon.png")

    for name in ("favicon-32.png", "favicon-192.png", "favicon.ico", "apple-touch-icon.png"):
        print(name, (ROOT / name).stat().st_size, "bytes")


if __name__ == "__main__":
    main()
