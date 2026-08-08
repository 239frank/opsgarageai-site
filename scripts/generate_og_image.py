from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "og-image.png"
WIDTH, HEIGHT = 1200, 630


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size=size)


def rounded_gradient(base: Image.Image, box: tuple[int, int, int, int], radius: int) -> None:
    x1, y1, x2, y2 = box
    panel = Image.new("RGBA", (x2 - x1, y2 - y1), (14, 31, 52, 242))
    mask = Image.new("L", panel.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, panel.width - 1, panel.height - 1), radius=radius, fill=255)
    base.alpha_composite(Image.composite(panel, Image.new("RGBA", panel.size), mask), (x1, y1))


def main() -> None:
    image = Image.new("RGBA", (WIDTH, HEIGHT), "#08111f")

    glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse((-170, -220, 620, 570), fill=(94, 234, 212, 58))
    glow_draw.ellipse((760, -180, 1380, 440), fill=(147, 197, 253, 45))
    glow = glow.filter(ImageFilter.GaussianBlur(95))
    image.alpha_composite(glow)

    draw = ImageDraw.Draw(image)
    draw.line((72, 92, 1128, 92), fill=(255, 255, 255, 30), width=1)

    logo = Image.open(ROOT / "assets" / "ops-garage-ai-logo.png").convert("RGBA")
    logo.thumbnail((270, 64), Image.Resampling.LANCZOS)
    image.alpha_composite(logo, (72, 21))

    accent = (94, 234, 212, 255)
    text = (238, 245, 255, 255)
    muted = (182, 196, 215, 255)
    draw.text((72, 142), "AI TRANSFORMATION FOR GROWING BUSINESSES", font=font("seguisb.ttf", 19), fill=accent)

    headline_font = font("seguisb.ttf", 62)
    draw.text((68, 188), "Turn AI into working", font=headline_font, fill=text)
    draw.text((68, 260), "business systems.", font=headline_font, fill=text)
    draw.text(
        (72, 356),
        "Find the manual work, missed follow-up, and handoff gaps.",
        font=font("segoeui.ttf", 24),
        fill=muted,
    )
    draw.text(
        (72, 392),
        "Build the right workflow around the tools you already use.",
        font=font("segoeui.ttf", 24),
        fill=muted,
    )

    rounded_gradient(image, (720, 132, 1128, 526), 22)
    panel = ImageDraw.Draw(image)
    panel.rounded_rectangle((720, 132, 1128, 526), radius=22, outline=(94, 234, 212, 78), width=2)
    panel.text((760, 172), "A PRACTICAL FIRST WIN", font=font("seguisb.ttf", 16), fill=accent)

    rows = [
        ("01", "Map the work", "See delays, owners, and failure points."),
        ("02", "Choose the right fix", "Avoid unnecessary tools and complexity."),
        ("03", "Build with control", "Keep approvals and fallback paths visible."),
    ]
    y = 222
    for number, title, body in rows:
        panel.text((760, y), number, font=font("seguisb.ttf", 16), fill=accent)
        panel.text((805, y - 4), title, font=font("seguisb.ttf", 23), fill=text)
        panel.text((805, y + 29), body, font=font("segoeui.ttf", 16), fill=muted)
        y += 92

    panel.rounded_rectangle((72, 500, 425, 558), radius=12, fill=accent)
    panel.text((98, 515), "opsgarageai.com", font=font("seguisb.ttf", 22), fill=(6, 32, 27, 255))
    panel.text((72, 583), "WORKFLOW AUTOMATION  •  TEAM ENABLEMENT  •  HUMAN REVIEW", font=font("seguisb.ttf", 15), fill=muted)

    image.convert("RGB").save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    main()
