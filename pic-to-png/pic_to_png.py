# Opera Soft's PIC to PNG image exporter.
# Converts from Opera Soft's MS-DOS games .PIC file to standard PNG. These files were typically loading screens for
# old games from the company.

import os, sys, time, argparse
import pic_to_png_conf as conf

from PIL import Image

PALETTE = conf.palettes['cga']
SIZE_X = 320
SIZE_Y = 200

DEBUG = False


def increment_counters(x_counter, y_counter, bpp):
    # TODO: Research reasoning behind even/odd lines storage
    # Maybe CGA allowed writing 2 different rows at once?
    # See: https://moddingwiki.shikadi.net/wiki/Raw_CGA_Data#Interlaced_CGA_Data
    x_counter += 1
    if x_counter == SIZE_X:
        x_counter = 0
        if (bpp == 2): # cga
          # jump 2 lines to make space for 2nd pass
          y_counter += 2
        elif (bpp == 4):
          y_counter += 1
    if y_counter == SIZE_Y:
        # Start 2nd pass, reading odd lines
        y_counter = 1
    return x_counter, y_counter


def write_pixel(byte_int, image_pixels, x_counter, y_counter):
    color = PALETTE[byte_int]
    if (not color):
      color = (0, 0, 0)

    if DEBUG:
        print(f"({x_counter},{y_counter}):{byte_int}:{color}")

    if y_counter < SIZE_Y:
        image_pixels[x_counter, y_counter] = color

    return image_pixels


def unpack_cga_pixel(data, index):
    if index == 0:
        return (data & 0b11000000) >> 6
    elif index == 1:
        return (data & 0b00110000) >> 4
    elif index == 2:
        return (data & 0b00001100) >> 2
    else:
        return (data & 0b00000011)


def unpack_linear_pixel(data, index):
    if index == 0:
        return (data & 0b11110000) >> 4
    else:
        return (data & 0b00001111)


def unpack_planar_pixel(byte1, byte2, byte3, byte4, bitIndex):
    mask = 0b10000000 >> bitIndex
    # amount of shift to get bit in first position
    shift = 8 - bitIndex - 1
    # shift the bits back into their position and combine them to get a value
    index = ((byte1 & mask) >> shift << 3) | ((byte2 & mask) >> shift << 2) | ((byte3 & mask) >> shift << 1) | ((byte4 & mask) >> shift)
    if DEBUG:
        print(index, f"{mask:08b}", shift, f"{byte1:08b}", f"{byte2:08b}", f"{byte3:08b}", f"{byte4:08b}", bitIndex, sep=",")
    return index


def handle_byte(byte, pixels, x_counter, y_counter, bpp):
    byte_int = int.from_bytes(byte, byteorder="little")
    if DEBUG:
        print(f"B: {byte_int:08b}")

    r = 4 if bpp == 2 else 2

    for pixel_num in range(r):
        # CGA is 4 colors == 2 bits per color, so 1 byte stores 4 pixels
        if (bpp == 2):
          pixel = unpack_cga_pixel(byte_int, pixel_num)
        # EGA is 16 colors == 4 bits per color, so 1 byte stores 2 pixels
        elif (bpp == 4):
          pixel = unpack_linear_pixel(byte_int, pixel_num)

        if DEBUG:
            print(f" @{x_counter},{y_counter}:  {pixel}->", end="")

        pixels = write_pixel(pixel, pixels, x_counter, y_counter)
        x_counter, y_counter = increment_counters(x_counter, y_counter, bpp)

    return pixels, x_counter, y_counter

def parseArgs():
    parser = argparse.ArgumentParser(description="Parses and converts various Operasoft PIC images.", add_help=False, epilog='Operasoft file naming conventions are handled automaticaly. Provide the relevant arguments when using other file names.')
    parser.add_argument('--help', action="help")
    parser.add_argument('-t', '--type', choices=["planar", "linear"], default="linear")
    parser.add_argument('-p', '--palette', choices=conf.palettes.keys(), help="Additional palettes can be added in pic_to_png_conf.py")
    parser.add_argument('-b', '--bpp', help='Bits per pixel: 2 for cga, 4 for ega.', choices=[2, 4], type=int, default=4)
    parser.add_argument('-w', '--width', help='Width of the image.', type=int, default=320)
    parser.add_argument('-h', '--height', help='Height of the image.', type=int, default=200)
    parser.add_argument('-o', '--outfile', help='Output filename, default appends ".png".')
    parser.add_argument('-f', '--filename', help='Input filename.')
    parser.add_argument('-d', '--debug', help='Enable debug ouput.')
    args = parser.parse_args()

    if (args.width and args.height):
      globals()['SIZE_X'] = args.width
      globals()['SIZE_Y'] = args.height

    return args


def parseFiles(args):
    pics = []
    files = []

    # get list of files from current directory or command line
    if (args.filename):
      files.append(args.filename)
    else:
      files = os.listdir(os.getcwd())

    # traverse files
    for file in files:
      # get the base name and extension for config checks
      basename = file[0:-4].lower()
      ext = file[-3:].upper()

      # get any command line args (or their defaults)
      bpp = args.bpp
      type = args.type
      palette = args.palette

      # found an operasoft image
      if (ext == 'PIC' or args.filename):

        # check if it follows the ega naming convention
        if (basename[-4:] == '_ega'):

          # config type takes precedence
          type = "planar"

          # strip _ega to get the base name for config checks
          basename = basename[0:-4]
          picConf = conf.pics.get(basename)

          # get the type override if present
          if (picConf != None):
            type = picConf.get('type', type)

          # determine palette if none is set
          if (palette == None):
            # check for a palette in conf and fallback to generic ega palette
            if (conf.palettes.get(basename) != None):
              palette = basename
            else: palette = 'ega'
        else:
          # use cga defaults
          bpp = 2
          type = 'linear'
          # check if there's a palette config
          if (palette == None):
            picConf = conf.pics.get(basename)
            # check for a palette in conf and fallback to generic cga palette if not
            if (picConf != None and picConf.get('palette') != None):
              palette = picConf['palette']
            else: palette = 'cga'

        pics.append({'type': type, 'filename': file, 'palette': palette, 'bpp': bpp})

    return pics


def export():
  args = parseArgs()
  pics = parseFiles(args)

  for pic in pics:
    x_counter = 0
    y_counter = 0
    image = Image.new("RGB", (SIZE_X, SIZE_Y))
    pixels = image.load()

    fn = pic['filename']
    globals()['PALETTE'] = conf.palettes.get(pic.get('palette', args.palette))

    print(f"Parsing file {fn} with a size of {SIZE_X}x{SIZE_Y}")

    with open(f"{fn}", "rb") as file_handle:
      bpp = pic['bpp']
      if pic['type'] == 'planar':
        chunkSize = int(SIZE_X * SIZE_Y / 8)

        # grab the four chunks of RGBI data
        bytes1 = file_handle.read(chunkSize)
        bytes2 = file_handle.read(chunkSize)
        bytes3 = file_handle.read(chunkSize)
        bytes4 = file_handle.read(chunkSize)

        # read one bit at a time from each chunk
        for b in range(chunkSize):
            for bitNum in range(8):
                index = unpack_planar_pixel(bytes1[b], bytes2[b], bytes3[b], bytes4[b], bitNum)
                pixels = write_pixel(index, pixels, x_counter, y_counter)
                x_counter, y_counter = increment_counters(x_counter, y_counter, bpp)
      else:
        byte = file_handle.read(1)
        while byte:
            pixels, x_counter, y_counter = handle_byte(byte, pixels, x_counter, y_counter, bpp)

            # After reading 1/2 of the image (the even lines), there are 768 pixels (192 bytes) of black before the odd lines start
            # SEE:  https://moddingwiki.shikadi.net/wiki/PIC_Format#PIC_format_version_0
            if bpp == 2 and x_counter == 0 and y_counter == 1:
                byte = file_handle.read(192)

            byte = file_handle.read(1)

    outfile = args.outfile or (fn + ".png")
    image.save(outfile)


if __name__ == "__main__":
    export()
