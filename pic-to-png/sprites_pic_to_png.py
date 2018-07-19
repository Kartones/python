# Opera Soft's sprites extracted from .COM executables to PNG image exporter.
# This is a total WIP, not yet finished. Based on 'pic_to_png.py'

from PIL import Image


FILENAME = "bigblock4"
SIZE_X = 8
SIZE_Y = 1600
# Outputs
DEBUG = False

PIXELS_TO_SKIP = 320*28 + 0


def increment_counters(x_counter, y_counter):
    x_counter += 1
    if x_counter == SIZE_X:
        x_counter = 0
        y_counter += 1
    # next sprite
    if y_counter == SIZE_Y:
        y_counter = 0
        x_counter = 0
    return x_counter, y_counter


# interlaced version, seems to be of no need with normal sprites, but left just in case until 100% sure.
def _increment_counters(x_counter, y_counter):
    x_counter += 1
    if x_counter == SIZE_X:
        x_counter = 0
        # jump 2 lines to make space for 2nd pass
        y_counter += 2
    if y_counter == SIZE_Y:
        # Start 2nd pass, reading odd lines
        y_counter = 1
    # next sprite
    if y_counter == SIZE_Y+1:
        y_counter = 0
        x_counter = 0
    return x_counter, y_counter


def store_pixel(byte_int, target_image, image_pixels, x_counter, y_counter):
    # CGA: https://en.wikipedia.org/wiki/Color_Graphics_Adapter#Color_palette
    color = (0, 0, 0)  # black
    if byte_int == 1:
        color = (85, 255, 255)  # cyan
    elif byte_int == 2:
        color = (255, 85, 255)  # magenta
    elif byte_int == 3:
        color = (255, 255, 255)  # white

    if y_counter < SIZE_Y:
        if DEBUG:
            print(f"({x_counter},{y_counter}):{color}")
        image_pixels[x_counter, y_counter] = color

    return target_image, image_pixels


def unpack_pixel_from_byte(data, pixel):
    if pixel == 0:
        return (data & 192) >> 6
    elif pixel == 1:
        return (data & 48) >> 4
    elif pixel == 2:
        return (data & 12) >> 2
    else:
        return (data & 3)


def operate_with_one_read_pixel(byte, image, pixels, x_counter, y_counter, skip_counter):
    byte_int = int.from_bytes(byte, byteorder="little")
    if DEBUG:
        print(f"B: {byte_int:08b}")

    # CGA == 4 colors == 2 bits, so 1 byte stores 4 pixels
    for pixel_num in range(4):
        pixel = unpack_pixel_from_byte(byte_int, pixel_num)
        if DEBUG:
            print(f"{pixel}->", end="")

        if skip_counter >= PIXELS_TO_SKIP:
            image, pixels = store_pixel(pixel, image, pixels, x_counter, y_counter)

        if skip_counter < PIXELS_TO_SKIP:
            skip_counter += 1
        else:
            x_counter, y_counter = increment_counters(x_counter, y_counter)

    return byte, image, pixels, x_counter, y_counter, skip_counter


def export():
    x_counter = 0
    y_counter = 0
    image = Image.new("RGB", (SIZE_X, SIZE_Y))
    pixels = image.load()

    skip_counter = 0
    sprite_counter = 0

    with open(f"samples/{FILENAME}", "rb") as file_handle:
        byte = file_handle.read(1)
        byte, image, pixels, x_counter, y_counter, skip_counter = operate_with_one_read_pixel(
            byte,
            image,
            pixels,
            x_counter,
            y_counter,
            skip_counter
        )

        while byte:
            byte = file_handle.read(1)
            byte, image, pixels, x_counter, y_counter, skip_counter = operate_with_one_read_pixel(
                byte,
                image,
                pixels,
                x_counter,
                y_counter,
                skip_counter
            )

            if x_counter == y_counter == 0 and skip_counter >= PIXELS_TO_SKIP:
                sprite_counter += 1
                image.save(f"spr_{FILENAME}_{sprite_counter}.png")

    # save last sprite
    image.save(f"spr_{FILENAME}_{sprite_counter}.png")

if __name__ == "__main__":
    export()
