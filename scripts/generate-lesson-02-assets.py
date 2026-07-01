#!/usr/bin/env python3
import base64
import os
import re
import subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(REPO, "assets", "lesson-02")
OUT_DIR = SRC_DIR

WRAPPER_WIDTH = 800
WRAPPER_HEIGHT = 600

MAPPING = [
    (
        "1_What_is_Product_Design_-ee2d1f33-5996-4961-8869-d123a0a14935.png",
        "what-to-build-vs-how-it-works.svg",
    ),
]


def png_to_svg(src: str, dst: str) -> None:
    width = int(
        re.search(
            r"pixelWidth: (\d+)",
            subprocess.check_output(["sips", "-g", "pixelWidth", src], text=True),
        ).group(1)
    )
    height = int(
        re.search(
            r"pixelHeight: (\d+)",
            subprocess.check_output(["sips", "-g", "pixelHeight", src], text=True),
        ).group(1)
    )
    scale = min(WRAPPER_WIDTH / width, WRAPPER_HEIGHT / height)
    draw_w = round(width * scale)
    draw_h = round(height * scale)
    x = (WRAPPER_WIDTH - draw_w) // 2
    y = (WRAPPER_HEIGHT - draw_h) // 2
    b64 = base64.b64encode(open(src, "rb").read()).decode("ascii")
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{WRAPPER_WIDTH}" height="{WRAPPER_HEIGHT}" '
        f'viewBox="0 0 {WRAPPER_WIDTH} {WRAPPER_HEIGHT}">\n'
        f'  <image x="{x}" y="{y}" width="{draw_w}" height="{draw_h}" '
        f'xlink:href="data:image/png;base64,{b64}"/>\n'
        "</svg>\n"
    )
    with open(dst, "w", encoding="utf-8") as handle:
        handle.write(svg)


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    for src_name, dst_name in MAPPING:
        src = os.path.join(SRC_DIR, src_name)
        if not os.path.isfile(src):
            raise FileNotFoundError(f"Missing source PNG: {src}")
        dst = os.path.join(OUT_DIR, dst_name)
        png_to_svg(src, dst)
        print(f"created {dst_name}")


if __name__ == "__main__":
    main()
