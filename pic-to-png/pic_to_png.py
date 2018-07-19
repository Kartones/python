# Opera Soft's PIC to PNG image exporter.
# Converts from Opera Soft's MS-DOS games .PIC file to standard PNG. These files were typically loading screens for
# old games from the company.

import time

from PIL import Image


FILENAME = "MUTAN_Z.PIC"
# FILENAME = "ABADIA.PIC"
# FILENAME = "SOL_CGA.PIC"
# FILENAME = "LIV2_CGA.PIC"
# FILENAME = "cor_cga.pic"
SIZE_X = 320
SIZE_Y = 200
# Outputs
DEBUG = False


def increment_counters(x_counter, y_counter):
    # TODO: Research reasoning behind even/odd lines storage
    # Maybe CGA allowed writing 2 different rows at once?
    x_counter += 1
    if x_counter == SIZE_X:
        x_counter = 0
        # jump 2 lines to make space for 2nd pass
        y_counter += 2
    if y_counter == SIZE_Y:
        # Start 2nd pass, reading odd lines
        y_counter = 1
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
    # I corroborated that I was on the right path checking http://www.abadiadelcrimen.com/vigasoco.html,
    # especifically the CPC sprite drawing in mode 1.

    # 00000011  1 + 2 =     3
    # 00001100  8 + 4 =    12
    # 00110000 16 + 32 =   48
    # 11000000 128 + 64 = 192
    if pixel == 0:
        return (data & 192) >> 6
    elif pixel == 1:
        return (data & 48) >> 4
    elif pixel == 2:
        return (data & 12) >> 2
    else:
        return (data & 3)


def operate_with_one_read_pixel(byte, image, pixels, x_counter, y_counter):
    byte_int = int.from_bytes(byte, byteorder="little")
    if DEBUG:
        print(f"B: {byte_int:08b}")

    # CGA == 4 colors == 2 bits, so 1 byte stores 4 pixels
    for pixel_num in range(4):
        pixel = unpack_pixel_from_byte(byte_int, pixel_num)
        if DEBUG:
            print(f"{pixel}->", end="")
        image, pixels = store_pixel(pixel, image, pixels, x_counter, y_counter)
        x_counter, y_counter = increment_counters(x_counter, y_counter)

    return byte, image, pixels, x_counter, y_counter


def export():
    x_counter = 0
    y_counter = 0
    image = Image.new("RGB", (SIZE_X, SIZE_Y))
    pixels = image.load()

    with open(f"samples/{FILENAME}", "rb") as file_handle:
        byte = file_handle.read(1)
        byte, image, pixels, x_counter, y_counter = operate_with_one_read_pixel(byte,
                                                                                image,
                                                                                pixels,
                                                                                x_counter,
                                                                                y_counter)

        while byte:
            byte = file_handle.read(1)
            byte, image, pixels, x_counter, y_counter = operate_with_one_read_pixel(byte,
                                                                                    image,
                                                                                    pixels,
                                                                                    x_counter,
                                                                                    y_counter)
            # TODO: research why this cleaning is needed.
            # After reading 1/2 of the image (the even lines), there are 768 pixels (192 bytes) of black before
            # the odd lines start
            if x_counter == 0 and y_counter == 1:
                byte = file_handle.read(192)

    image.save(f"FILENAME_{time.time()}.png")


if __name__ == "__main__":
    export()
