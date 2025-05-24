from rembg import remove, new_session
from PIL import Image, ImageFilter
from pathlib import Path
import os

# === SETTINGS ===
MODEL_NAME = "u2net"  # Options: "u2net", "u2netp", "isnet-general-use"
UPSCALE_FACTOR = 2  # Use 1 for no upscaling
SMOOTH_EDGES = True
MAX_DIMENSION = 1024  # Resize longest side if image is bigger
SUPPORTED_EXTS = ['.jpg', '.jpeg', '.png']
INPUT_FOLDER = Path('input_images')
OUTPUT_FOLDER = Path('output_images')


def resize_image(img, max_dimension):
    if max(img.size) > max_dimension:
        ratio = max_dimension / float(max(img.size))
        new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
        img = img.resize(new_size, Image.LANCZOS)
    return img


def upscale_image(img, factor):
    if factor > 1:
        new_size = (img.width * factor, img.height * factor)
        img = img.resize(new_size, Image.LANCZOS)
    return img


def smooth_edges(img):
    return img.filter(ImageFilter.GaussianBlur(radius=0.5))


def process_image(input_path: Path, output_folder: Path, session):
    with open(input_path, 'rb') as f:
        input_data = f.read()
        output_data = remove(input_data, session=session)

    # Save PNG version
    output_png_path = output_folder / f'{input_path.stem}_no_bg.png'
    with open(output_png_path, 'wb') as out_file:
        out_file.write(output_data)

    # Open for post-processing
    img = Image.open(output_png_path).convert("RGBA")

    # Resize if needed
    img = resize_image(img, MAX_DIMENSION)

    # Smoothen edges
    if SMOOTH_EDGES:
        img = smooth_edges(img)

    # Upscale
    img = upscale_image(img, UPSCALE_FACTOR)

    # Save final PNG
    img.save(output_png_path, format='PNG')

    # Save WebP
    output_webp_path = output_folder / f'{input_path.stem}_no_bg.webp'
    img.save(output_webp_path, format='WEBP')

    print(f"✅ Processed: {input_path.name}")


def batch_process(input_folder: Path, output_folder: Path):
    output_folder.mkdir(exist_ok=True)
    session = new_session(model_name=MODEL_NAME)

    files = list(input_folder.glob('*'))
    image_files = [f for f in files if f.suffix.lower() in SUPPORTED_EXTS]

    if not image_files:
        print("⚠️ No supported image files found.")
        return

    for file in image_files:
        try:
            process_image(file, output_folder, session)
        except Exception as e:
            print(f"❌ Failed: {file.name} — {e}")


if __name__ == "__main__":
    print("🚀 Starting batch background removal...")
    batch_process(INPUT_FOLDER, OUTPUT_FOLDER)
    print("🎉 All done!")