from PIL import Image, ImageFilter, ImageDraw

def process_image(input_path: str, output_path: str):

    image = Image.open(input_path)

    rotated = image.rotate(45)

    filtered = rotated.filter(ImageFilter.EMBOSS)

    draw = ImageDraw.Draw(filtered)

    draw.text((20, 20), "UCV - Sistemas Inteligentes", fill="white")

    filtered.save(output_path)

    return output_path