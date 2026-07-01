#!/usr/bin/env python3
import base64
import os
import re
import subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = "/Users/ishii/.cursor/projects/Users-ishii-Downloads-monad-build-anything-uiux-intro/assets"
OUT_DIR = os.path.join(REPO, "assets", "lesson-02")

MAPPING = [
    ("1_What_is_Product_Design_-ee2d1f33-5996-4961-8869-d123a0a14935.png", "what-is-product-design.svg"),
    ("1_What_is_UIUX_Design_-8a2a3ff9-9680-466b-aa9f-f40af30b6619.png", "what-to-build-vs-how-it-works.svg"),
    ("2_Why_UIUX_Matters-f9265c92-3573-4ea9-b3ab-c33d48b91baa.png", "define-success.svg"),
    ("3_Understanding_Users-48d263e9-03d6-468e-b31b-5ae5e8d2e01d.png", "start-with-problems.svg"),
    ("4_Information_Architecture__IA_-faf875cb-235f-4d8d-8095-c82fb18bfa14.png", "mvp-and-prioritization.svg"),
    ("5_Designing_User_Flows-401e5f6a-d8eb-417a-8591-9b8be471f3d5.png", "making-product-decisions.svg"),
    ("6_Creating_the_Interface-872075b6-0a94-4a8c-8d1e-d4f6399e55bf.png", "testing-beyond-mockups.svg"),
    ("7_Testing_and_Iteration-af86ccee-66d9-474e-b7b3-bb7bb43337ac.png", "testing-assumptions.svg"),
]


def png_to_svg(src: str, dst: str) -> None:
    width = int(re.search(r"pixelWidth: (\d+)", subprocess.check_output(
        ["sips", "-g", "pixelWidth", src], text=True
    )).group(1))
    height = int(re.search(r"pixelHeight: (\d+)", subprocess.check_output(
        ["sips", "-g", "pixelHeight", src], text=True
    )).group(1))
    b64 = base64.b64encode(open(src, "rb").read()).decode("ascii")
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{width}" height="{height}" viewBox="0 0 {width} {height}">\n'
        f'  <image width="{width}" height="{height}" xlink:href="data:image/png;base64,{b64}"/>\n'
        "</svg>\n"
    )
    with open(dst, "w", encoding="utf-8") as handle:
        handle.write(svg)


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    for src_name, dst_name in MAPPING:
        src = os.path.join(SRC_DIR, src_name)
        dst = os.path.join(OUT_DIR, dst_name)
        png_to_svg(src, dst)
        print(f"created {dst_name}")


if __name__ == "__main__":
    main()
