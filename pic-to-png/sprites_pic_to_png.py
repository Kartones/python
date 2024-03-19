# Opera Soft's sprites extracted from .COM executables to PNG image exporter.
# This is a WIP. Based on 'pic_to_png.py'

import os, sys, time, argparse
from PIL import Image

DEBUG = False
OUTDIR = "sprites"

def increment_counters(x_counter, y_counter, width, height):
    x_counter += 1
    if x_counter == width:
        x_counter = 0
        y_counter += 1
    # next sprite
    if y_counter >= height:
        y_counter = 0
        x_counter = 0
    return x_counter, y_counter


def store_pixel(byte_int, image_pixels, x_counter, y_counter):
    # CGA: https://en.wikipedia.org/wiki/Color_Graphics_Adapter#Color_palette
    color = (0, 0, 0)  # black
    if byte_int == 1:
        color = (85, 255, 255)  # cyan
    elif byte_int == 2:
        color = (255, 85, 255)  # magenta
    elif byte_int == 3:
        color = (255, 255, 255)  # white

    image_pixels[x_counter, y_counter] = color

    return image_pixels


def unpack_pixel_from_byte(data, pixel):
    if pixel == 0:
        return (data & 192) >> 6
    elif pixel == 1:
        return (data & 48) >> 4
    elif pixel == 2:
        return (data & 12) >> 2
    else:
        return (data & 3)


def operate_with_one_read_pixel(byte_int, pixels, x_counter, y_counter, width, height):
    #if DEBUG:
    #    print(f"{byte_int:02X} {byte_int:08b}", end=" ")

    # CGA == 4 colors, 2 bits per color; so 1 byte stores 4 pixels
    for pixel_num in range(4):

        pixel = unpack_pixel_from_byte(byte_int, pixel_num)
        #if DEBUG:
        #    print(f"{pixel}", end="")

        pixels = store_pixel(pixel, pixels, x_counter, y_counter)

        x_counter, y_counter = increment_counters(x_counter, y_counter, width, height)

    #if DEBUG:
    #    print("")

    return pixels, x_counter, y_counter


def process_image_data(basename, file_handle, width, height, max=1):

    images = []
    image = Image.new("RGB", (width, height))
    pixels = image.load()
    x_counter = 0
    y_counter = 0

    sprite_counter = 0

    pointer = file_handle.tell()

    if DEBUG:
        pointer = file_handle.tell()
        print(f"{width}x{height} @ {pointer:04X}")

    byte = file_handle.read(1)

    while byte:
        pixels, x_counter, y_counter = operate_with_one_read_pixel(
            byte[0], pixels, x_counter, y_counter, width, height
        )

        if x_counter == y_counter == 0:

            end_byte = file_handle.tell() - 1
            name = basename.format(count=sprite_counter)
            data_pointer = pointer + 0x0100 - 2
            image.save(f"{OUTDIR}/{name}_{pointer:04X}-{end_byte:04X}_{data_pointer:04X}.png")
            images.append(image.copy())

            pointer = file_handle.tell()
            sprite_counter += 1

        if sprite_counter == max:
            break

        byte = file_handle.read(1)

    return images


def process_sprites_data(file_handle, max):

  # process sprites
  count = 0
  done = False
  while not done:

    # first two bytes are width and height in pixels, width is shifted two bits
    width = file_handle.read(1)[0] << 2
    height = file_handle.read(1)[0]

    # save the sprite
    process_image_data(f'sprite_{count:03}', file_handle, width, height)

    count += 1

    # end processing after the last sprite
    if count >= max:
      done = True


def process_block_data(file_handle, offsetStart, max, tiles):

  # process blocks
  count = 0
  done = False
  blocks = {}
  while not done:

    # store the starting file position of this block
    start = file_handle.tell()

    # get width and height of block in tiles
    width = file_handle.read(1)[0]
    height = file_handle.read(1)[0]

    # create the new image with each tile being 8x8 pixels
    block = Image.new("RGB", (width * 8, height * 8))

    if DEBUG:
      print(f'block {width:02}x{height:02} @ {start:04X}')

    # traverse through the tile references, left to right, top to bottom
    for y in range(height):
      for x in range(width):
        # we already indexed the tiles earlier so get the reference and look it up
        tileIndex = file_handle.read(1)[0]
        tile = tiles[tileIndex]
        # paste the tile in to the correct location
        block.paste(tile, (x * 8, y * 8))

    # store the ending file position of this block
    end = file_handle.tell() - 1

    # the offset is a hardcoded value in the original source
    offset = start - offsetStart + 0x0100

    # save it with some important details in the filename
    block.save(f"{OUTDIR}/block_{count:03}_{start:04X}-{end:04X}_{offset:04X}.png")

    # save reference to block for room generation
    blocks[offset] = block

    count += 1

    # end processing after the last block
    if count > max:
      done = True

  return blocks


def process_screens_data(file_handle, dataAddr, max, blocks, hud):

  nextAddr = file_handle.tell()

  # process rooms
  count = 0
  done = False
  while not done:

    # traverse through 2 byte offsets for each room
    file_handle.seek(nextAddr)
    offset = int.from_bytes(file_handle.read(2), byteorder="little")
    nextAddr += 2

    # add the offset to the hardcoded source value and start parsing the room data
    roomAddr = dataAddr + offset
    file_handle.seek(roomAddr)
    numBlocks = file_handle.read(1)[0]

    # store the starting file position of this room
    start = file_handle.tell()

    #if count == 0x1B:
    if DEBUG:
      print(f'Generating screen 0x{count:02X} @ {roomAddr:04X} (offset {offset:04X}) with 0x{numBlocks:02X} blocks')

    room = Image.new("RGB", (320, 200))

    for b in range(numBlocks):
      # store the starting file position of this block
      block_addr = file_handle.tell()

      # get the x and y block position (in tiles, not pixels)
      x = file_handle.read(1)[0]
      y = file_handle.read(1)[0]

      # we already indexed the blocks earlier so get the reference and look it up
      offset = int.from_bytes(file_handle.read(2), byteorder="little")
      block = blocks[offset]

      #if count == 0x1B:
      if DEBUG:
        print(f'  Generating block {offset:04X} [{block_addr:04X}] @ {x:02X},{y:02X} ({x}, {y})')

      # paste the block in
      room.paste(block, (x * 8, y * 8))

    # include the hud at bottom
    # TODO remove?
    room.paste(hud, (0, 160))

    # save the file with a few important details
    end = file_handle.tell() - 1
    room.save(f"{OUTDIR}/screen_{count:02X}_{start:04X}-{end:04X}.png")

    count += 1

    if count > max:
      done = True


def parse_goody(filename):

  if filename == None:
    filename = "GOODY.OVL"

  with open(filename, "rb") as file_handle:

    # process the tiles, saving the references for block processing
    file_handle.seek(0x62C2)
    tiles = process_image_data('tile_{count:03}_{count:02X}', file_handle, 8, 8, 316)

    # process blocks and hold on to them for rooms
    file_handle.seek(0x7683)
    blocks = process_block_data(file_handle, 0x7782, 138, tiles)

    # process hud and hold onto the reference for screens
    file_handle.seek(0xE063)
    hud = process_image_data('hud', file_handle, 320, 40)[0]

    # process rooms
    file_handle.seek(0x6236)
    process_screens_data(file_handle, 0x477B, 0x45, blocks, hud)

    # process sprites
    file_handle.seek(0x8578)
    process_sprites_data(file_handle, 159)


def parse_mutan(filename):

  if filename == None:
    filename = "MUTAN_Z1.OVL"

  with open(filename, "rb") as file_handle:

    # process the tiles
    file_handle.seek(0x9044)
    process_image_data('tile_{count:03}_{count:02X}', file_handle, 8, 8, 256)

    # process the cockpit tiles
    file_handle.seek(0xA8FF)
    process_image_data('cockpit_{count:02}_{count:02X}', file_handle, 8, 8, 48)

    # process the text tiles
    file_handle.seek(0xACBA)
    process_image_data('text_{count:02}_{count:02X}', file_handle, 8, 8, 36)

    # process the lizard man
    file_handle.seek(0xCA6D)
    process_image_data('arm', file_handle, 8, 56, 1)
    file_handle.seek(0xCADF)
    process_image_data('tail', file_handle, 8, 160, 1)
    file_handle.seek(0xC1EB)
    process_image_data('body', file_handle, 272, 32, 1)

    # process hud
    file_handle.seek(0xAEFA)
    process_sprites_data(file_handle, 1)


def dec(val):
  return int(val, 16)


def parse_args():

    parser = argparse.ArgumentParser(description="Parses and converts various Operasoft image formats.", add_help=False, epilog='Pass the relevant arguments or game name to begin parsing images.')

    parser.add_argument('--help', action="help")
    parser.add_argument('-a', '--address', help='Address of first image, in hex format, e.g. 0xA03F.', type=dec)
    parser.add_argument('-b', '--basename', help='Basename of the image(s).', default='image')
    parser.add_argument('-c', '--count', help='Max number of images to parse.', type=int, default=1)
    parser.add_argument('-w', '--width', help='Width of the image(s).', type=int, default=8)
    parser.add_argument('-h', '--height', help='Height of the image(s).', type=int, default=8)
    parser.add_argument('-f', '--filename', help='Input filename.')
    parser.add_argument('-o', '--outdir', help='Output directory.', default='sprites')
    parser.add_argument('-s', '--sprites', help='Parse as sprite data with two leading bytes of height and width information followed by the image data.', action='store_true')
    parser.add_argument('-g', '--game', choices=["goody", "mutan"])
    parser.add_argument('-d', '--debug', help='Enable debug ouput.', action='store_true')

    args = parser.parse_args()

    return parser, args


def export():
  parser, args = parse_args()

  if args.debug:
    globals()['DEBUG'] = True

  if args.outdir:
    if not os.path.isdir(args.outdir):
      os.makedirs(args.outdir)
    globals()['OUTDIR'] = args.outdir

  if args.game == "goody":
    parse_goody(args.filename)
  elif args.game == "mutan":
    parse_mutan(args.filename)
  elif args.filename and args.address:
    with open(args.filename, "rb") as file_handle:
      file_handle.seek(args.address)
      if args.sprites:
        process_sprites_data(file_handle, args.count)
      else:
        process_image_data(args.basename, file_handle, args.width, args.height, args.count)
  else:
    parser.print_help()


if __name__ == "__main__":
    export()
