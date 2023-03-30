"""A simple cli to convert pdf to images and back."""
__version__ = "0.1.0"
import os
from pdf2image import convert_from_path
from PIL import Image
import contextlib
from typer import Typer
from rich.console import Console

console = Console()
cli = Typer()


def resolv_path(path: str) -> tuple[str, str]:
    dest = os.path.dirname(path)
    file = os.path.basename(path)
    filename, *_ = file.partition('.')
    return dest, filename


@cli.command("pdf-to-img")
def convert_pdf_to_img(path: str) -> list[str]:
    dest, filename = resolv_path(path)
    pages = convert_from_path(path)
    files = []
    for idx, page in enumerate(pages):
        file = os.path.join(dest, f'{filename}_{idx}.jpg')
        page.save(file, 'JPEG')
        files.append(file)
    console.print(path, "converted to", ", ".join(files))
    return files

@cli.command("imgs-to-pdf")
def convert_imgs_to_pdf(images_path: list[str]) -> str:
    dest, filename = resolv_path(images_path[0])
    filebase, *_ = filename.rpartition('_')
    with contextlib.ExitStack() as stack:
        img_list = []
        for image_path in images_path:
            img = Image.open(image_path)
            stack.enter_context(img)
            img.convert('RGB')
            img_list.append(img)
        file = os.path.join(dest, f'{filebase}.pdf')
        img_list[0].save(file, save_all=True, append_images=img_list[1:])
    console.print(", ".join(images_path), "merged in", file)
    return file
