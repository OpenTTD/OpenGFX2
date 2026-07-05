#!/usr/bin/env python3

from PIL import Image, ImageDraw
import os, sys

from tools import check_update_needed, blue_to

def cursors_cursoroverlay(base_path, scale, verbose=True):
  print("Cursors", base_path)
  if os.path.isdir(os.path.join(base_path)) == False: os.mkdir(os.path.join(base_path))
  if os.path.isdir(os.path.join(base_path, "pygen")) == False: os.mkdir(os.path.join(base_path, "pygen"))

  tile_width = 36
  tile_height = 36
  icon_width = 20
  icon_height = 20

  cursor_list = {
    "default": "classic_yellow",
    "opengfx_yellow": "opengfx_yellow",
    "classic_gray": "classic_gray",
    "windows_white": "windows_white"
  }

  xoffset_list = {
    "classic_yellow": 8,
    "opengfx_yellow": 7,
    "classic_gray": 8,
    "windows_white": 7
  }
  yoffset_list = {
    "classic_yellow": 9,
    "opengfx_yellow": 16,
    "classic_gray": 9,
    "windows_white": 16,
  }

  icon_images_base = os.path.join(base_path, "..", "..", "icons", str(scale), "icons_20px")
  icon_map = [
    {"sx": 6, "sy": 0, "tx": 0, "ty": 1}, # question mark
    {"sx": 8, "sy": 6, "tx": 1, "ty": 1}, # company HQ
    {"sx": 7, "sy": 6, "tx": 2, "ty": 1}, # sign
    {"sx": 6, "sy": 6, "tx": 3, "ty": 1}, # town
    {"sx": 3, "sy": 6, "tx": 4, "ty": 1}, # industry
    {"sx": 0, "sy": 15, "tx": 5, "ty": 1}, # rocks
    {"sx": 1, "sy": 15, "tx": 6, "ty": 1}, # lighthouse
    {"sx": 2, "sy": 15, "tx": 7, "ty": 1}, # transmitter
    {"sx": 3, "sy": 15, "tx": 8, "ty": 1}, # purchase land
    {"sx": 6, "sy": 15, "tx": 9, "ty": 1}, # desert
    {"sx": 4, "sy": 6, "tx": 10, "ty": 1}, # trees
    {"sx": 1, "sy": 2, "tx": 0, "ty": 2}, # raise terrain 1
    {"sx": 5, "sy": 3, "tx": 1, "ty": 2}, # raise terrain 2
    {"sx": 6, "sy": 3, "tx": 2, "ty": 2}, # raise terrain 3
    {"sx": 2, "sy": 2, "tx": 3, "ty": 2}, # lower terrain 1
    {"sx": 7, "sy": 3, "tx": 4, "ty": 2}, # lower terrain 2
    {"sx": 8, "sy": 3, "tx": 5, "ty": 2}, # lower terrain 3
    {"sx": 5, "sy": 2, "tx": 6, "ty": 2}, # level terrain
    {"sx": 3, "sy": 2, "tx": 0, "ty": 3}, # demolish 1
    {"sx": 6, "sy": 2, "tx": 1, "ty": 3}, # demolish 2
    {"sx": 7, "sy": 2, "tx": 2, "ty": 3}, # demolish 3
    {"sx": 8, "sy": 2, "tx": 3, "ty": 3}, # demolish 4
    {"sx": 4, "sy": 5, "tx": 0, "ty": 4}, # go to 1
    {"sx": 5, "sy": 5, "tx": 1, "ty": 4}, # go to 2
    {"sx": 6, "sy": 5, "tx": 2, "ty": 4}, # go to 3
    {"sx": 5, "sy": 8, "tx": 0, "ty": 5}, # signals 1
    {"sx": 8, "sy": 7, "tx": 1, "ty": 5}, # signals 2
    {"sx": 1, "sy": 8, "tx": 0, "ty": 6}, # road depot
    {"sx": 3, "sy": 14, "tx": 1, "ty": 6}, # road \
    {"sx": 1, "sy": 14, "tx": 2, "ty": 6}, # road /
    {"sx": 4, "sy": 14, "tx": 5, "ty": 6}, # road tunnel
    {"sx": 5, "sy": 14, "tx": 6, "ty": 6}, # road auto
    {"sx": 6, "sy": 14, "tx": 7, "ty": 6}, # road replace
    {"sx": 6, "sy": 7, "tx": 8, "ty": 6}, # road bus stop
    {"sx": 5, "sy": 7, "tx": 9, "ty": 6}, # road lorry stop
    {"sx": 5, "sy": 21, "tx": 10, "ty": 6}, # road clone
    {"sx": 3, "sy": 13, "tx": 1, "ty": 7}, # tram \
    {"sx": 1, "sy": 13, "tx": 2, "ty": 7}, # tram /
    {"sx": 5, "sy": 13, "tx": 6, "ty": 7}, # tram auto
    {"sx": 6, "sy": 13, "tx": 7, "ty": 7}, # tram replace
    {"sx": 7, "sy": 9, "tx": 0, "ty": 8}, # rail depot
    {"sx": 0, "sy": 9, "tx": 1, "ty": 8}, # rail |
    {"sx": 1, "sy": 9, "tx": 2, "ty": 8}, # rail /
    {"sx": 2, "sy": 9, "tx": 3, "ty": 8}, # rail -
    {"sx": 3, "sy": 9, "tx": 4, "ty": 8}, # rail \
    {"sx": 4, "sy": 9, "tx": 5, "ty": 8}, # rail tunnel
    {"sx": 5, "sy": 9, "tx": 6, "ty": 8}, # rail auto
    {"sx": 6, "sy": 9, "tx": 7, "ty": 8}, # rail replace
    {"sx": 7, "sy": 7, "tx": 8, "ty": 8}, # rail station
    {"sx": 6, "sy": 8, "tx": 9, "ty": 8}, # rail waypoint
    {"sx": 4, "sy": 21, "tx": 10, "ty": 8}, # rail clone
    {"sx": 7, "sy": 10, "tx": 0, "ty": 9}, # elrail depot
    {"sx": 0, "sy": 10, "tx": 1, "ty": 9}, # elrail |
    {"sx": 1, "sy": 10, "tx": 2, "ty": 9}, # elrail /
    {"sx": 2, "sy": 10, "tx": 3, "ty": 9}, # elrail -
    {"sx": 3, "sy": 10, "tx": 4, "ty": 9}, # elrail \
    {"sx": 4, "sy": 10, "tx": 5, "ty": 9}, # elrail tunnel
    {"sx": 5, "sy": 10, "tx": 6, "ty": 9}, # elrail auto
    {"sx": 6, "sy": 10, "tx": 7, "ty": 9}, # elrail replace
    {"sx": 7, "sy": 11, "tx": 0, "ty": 10}, # monorail depot
    {"sx": 0, "sy": 11, "tx": 1, "ty": 10}, # monorail |
    {"sx": 1, "sy": 11, "tx": 2, "ty": 10}, # monorail /
    {"sx": 2, "sy": 11, "tx": 3, "ty": 10}, # monorail -
    {"sx": 3, "sy": 11, "tx": 4, "ty": 10}, # monorail \
    {"sx": 4, "sy": 11, "tx": 5, "ty": 10}, # monorail tunnel
    {"sx": 5, "sy": 11, "tx": 6, "ty": 10}, # monorail auto
    {"sx": 6, "sy": 11, "tx": 7, "ty": 10}, # monorail replace
    {"sx": 7, "sy": 12, "tx": 0, "ty": 11}, # maglev depot
    {"sx": 0, "sy": 12, "tx": 1, "ty": 11}, # maglev |
    {"sx": 1, "sy": 12, "tx": 2, "ty": 11}, # maglev /
    {"sx": 2, "sy": 12, "tx": 3, "ty": 11}, # maglev -
    {"sx": 3, "sy": 12, "tx": 4, "ty": 11}, # maglev \
    {"sx": 4, "sy": 12, "tx": 5, "ty": 11}, # maglev tunnel
    {"sx": 5, "sy": 12, "tx": 6, "ty": 11}, # maglev auto
    {"sx": 6, "sy": 12, "tx": 7, "ty": 11}, # maglev replace
    {"sx": 6, "sy": 21, "tx": 10, "ty": 10}, # ship clone
    {"sx": 7, "sy": 21, "tx": 10, "ty": 11}, # aircraft clone
    {"sx": 3.5, "sy": 7, "tx": 0, "ty": 12}, # airport
    {"sx": 2, "sy": 8, "tx": 0, "ty": 13}, # waterway depot
    {"sx": 3, "sy": 8, "tx": 1, "ty": 13}, # waterway lock
    {"sx": 7, "sy": 8, "tx": 2, "ty": 13}, # waterway canal
    {"sx": 4, "sy": 15, "tx": 3, "ty": 13}, # waterway river
    {"sx": 0, "sy": 2, "tx": 4, "ty": 13}, # waterway bouy
    {"sx": 2, "sy": 7, "tx": 8, "ty": 13}, # waterway dock
    {"sx": 5, "sy": 4, "tx": 0, "ty": 14}, # bridge
    {"sx": 8, "sy": 8, "tx": 2, "ty": 14}, # aqueduct
  ]

  def drawBackground(draw, x, y):
    draw.rectangle((((tile_width + 1) * x + 1) * scale, ((tile_height + 1) * y + 1) * scale, ((tile_width + 1) * (x + 1) + 1) * scale - scale - 1, ((tile_height + 1) * (y + 1) + 1) * scale - scale - 1), fill=(0, 0, 255), outline=None, width=scale)

  print("Running in scale "+str(scale)+" mode")
  print("Icons", str(scale))
  for cursor_key in cursor_list:
    print(" ", cursor_list[cursor_key])
    # for each cursor style
    xo = xoffset_list[cursor_list[cursor_key]]
    yo = yoffset_list[cursor_list[cursor_key]]
    cursor_cursor = os.path.join(base_path, cursor_list[cursor_key]+"_cursor.png")
    cursor_icon = os.path.join(base_path, cursor_list[cursor_key]+"_icon.png")
    cursor_wait = os.path.join(base_path, cursor_list[cursor_key]+"_wait.png")
    icon_base = icon_images_base+"_32bpp.png"
    icon_base_palmask = icon_images_base+"_palmask.png"
    output_name = os.path.join(base_path, "pygen", cursor_key+"_32bpp.png")
    output_name_palmask = os.path.join(base_path, "pygen", cursor_key+"_palmask.png")
    if check_update_needed([__file__, cursor_cursor, cursor_icon, cursor_wait, icon_base, icon_base_palmask], output_name):
      print("  Generating", os.path.basename(output_name))
      # determine size of output image
      max_x = 0
      max_y = 0
      for icon in icon_map:
        max_x = max(max_x, icon["tx"])
        max_y = max(max_y, icon["ty"])
      for type in ["32bpp", "palmask"]:
        # analyse twice, once normal, once for palmask
        print("  ", type)
        icon_base_path = icon_base
        if type == "palmask":
          icon_base_path = icon_base_palmask
        # make output image
        icons_image = Image.new("RGB", (scale * ((max_x + 1) * (tile_width + 1) + 1), scale * ((max_y + 1) * (tile_height + 1) + 1)), color=(255, 255, 255))
        draw = ImageDraw.Draw(icons_image)
        # special case cursors
        drawBackground(draw, 0, 0)
        image_cursor = Image.open(cursor_cursor).convert("RGB")
        icons_image = blue_to(image_cursor, 0, 0, image_cursor.size[0], image_cursor.size[1], icons_image, 0 * (tile_width + 1) + 1, 0 * (tile_height + 1) + 1, scale)
        drawBackground(draw, 1, 0)
        image_wait = Image.open(cursor_wait).convert("RGB")
        icons_image = blue_to(image_wait, 0, 0, image_wait.size[0], image_wait.size[1], icons_image, 1 * (tile_width + 1) + 1, 0 * (tile_height + 1) + 1, scale)
        # draw all icon cursors
        image_icon = Image.open(cursor_icon).convert("RGB")
        image_base = Image.open(icon_base_path).convert("RGB")
        for icon in icon_map:
          drawBackground(draw, icon["tx"], icon["ty"])
          blue_to(image_icon, 0, 0, image_icon.size[0], image_icon.size[0], icons_image, icon["tx"] * (tile_width + 1) + 1, icon["ty"] * (tile_height + 1) + 1, scale)
          blue_to(image_base, icon["sx"] * (icon_width + 1) + 1, icon["sy"] * (icon_height + 1) + 1, icon_width, icon_height, icons_image, icon["tx"] * (tile_width + 1) + 1 + xo, icon["ty"] * (tile_height + 1) + 1 + yo, scale)
          print("   ", "icon", icon["tx"], icon["ty"], icon["sx"], icon["sy"], icon["sx"] * (icon_width + 1) + 1, icon["sy"] * (icon_height + 1) + 1)
        # Save 32bpp image
        if type == "32bpp":
          icons_image.save(output_name)
        else:
          icons_image.save(output_name_palmask)
    else:
      print("  ", "Skipped", os.path.basename(output_name))

if __name__ == "__main__":
  if len(sys.argv) < 2:
    cursors_cursoroverlay(".", int(sys.argv[1]))
  else:
    cursors_cursoroverlay(sys.argv[2], int(sys.argv[1]))
