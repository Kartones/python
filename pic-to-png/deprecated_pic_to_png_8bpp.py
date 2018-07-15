# tries to import MS-DOS Opera Soft games .PIC files and save individual sprites as PNGs

import time

# pip3 install pillow
from PIL import Image


# FILENAME = "ABADIA.PIC"
FILENAME = "ABADIA.PIC"
SIZE_X = 8
SIZE_Y = 16


def increment_counters(x_counter, y_counter):
    sprite_finished = False
    x_counter += 1
    if x_counter == SIZE_X:
        x_counter = 0
        y_counter += 1
    if y_counter == SIZE_Y:
        y_counter = 0
        sprite_finished = True
    return x_counter, y_counter, sprite_finished


def store_pixel(byte_int, target_image, image_pixels, x_counter, y_counter, sprite_finished):
    if x_counter == y_counter == 0 and not sprite_finished:
        target_image = Image.new("RGB", (SIZE_X, SIZE_Y))
        image_pixels = target_image.load()

    if byte_int == 0:
        color = (0, 0, 0)  # black
    elif byte_int == 255:
        color = (255, 255, 255)  # white
    else:
        color = (0, byte_int, 0)

    image_pixels[x_counter, y_counter] = color

    if sprite_finished:
        target_image.save(f"{time.time()}.png")

    return target_image, image_pixels


def operate_with_one_read_pixel(byte, image, pixels, x_counter, y_counter, sprite_finished):
    byte_int = int.from_bytes(byte, byteorder="little")

    image, pixels = store_pixel(byte_int, image, pixels, x_counter, y_counter, sprite_finished)
    x_counter, y_counter, sprite_finished = increment_counters(x_counter, y_counter)

    return byte, image, pixels, x_counter, y_counter, sprite_finished


def read_and_print():
    x_counter = 0
    y_counter = 0
    sprite_finished = False
    image = None
    pixels = None

    with open(FILENAME, "rb") as file_handle:
        byte = file_handle.read(1)
        # byte, image, pixels, x_counter, y_counter, sprite_finished = \
        #     operate_with_one_read_pixel(byte, image, pixels, x_counter, y_counter, sprite_finished)

        while byte:
            byte = file_handle.read(1)
            byte, image, pixels, x_counter, y_counter, sprite_finished = \
                operate_with_one_read_pixel(byte, image, pixels, x_counter, y_counter, sprite_finished)


read_and_print()
