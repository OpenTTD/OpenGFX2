#!/usr/bin/env python3

from PIL import Image
import os, sys

from tools import check_update_needed, blend_overlay, blendmode_overlay, paste_to

def terrain_gridoverlay(scale, base_path=".", verbose=True):
  print("Terrain grids", base_path)
  if os.path.isdir(os.path.join(base_path)) == False: os.mkdir(os.path.join(base_path))
  if os.path.isdir(os.path.join(base_path, "pygen")) == False: os.mkdir(os.path.join(base_path, "pygen"))

  tile_size = scale * 64

  # Terrain sprites to use
  terrain_list = {
    "farm_groundtiles": "farm_groundtiles_32bpp.png",
    "arctic_groundtiles": "arctic_groundtiles_32bpp.png",
    "arctic_groundtiles_rocks": "arctic_groundtiles_rocks_32bpp.png",
    "arctic_groundtiles_rocks_alt": "arctic_groundtiles_rocks_alt_32bpp.png",
    "arctic_groundtiles_rough": "arctic_groundtiles_rough_32bpp.png",
    "arctic_groundtiles_snow": "arctic_groundtiles_snow_32bpp.png",
    "arctic_groundtiles_deserttransition": "arctic_groundtiles_deserttransition_32bpp.png",
    "arctic_groundtiles_snowtransition": "arctic_groundtiles_snowtransition_32bpp.png",
    "tropical_groundtiles": "tropical_groundtiles_32bpp.png",
    "tropical_groundtiles_rocks": "tropical_groundtiles_rocks_32bpp.png",
    "tropical_groundtiles_rocks_alt": "tropical_groundtiles_rocks_alt_32bpp.png",
    "tropical_groundtiles_rough": "tropical_groundtiles_rough_32bpp.png",
    "tropical_groundtiles_desert": "tropical_groundtiles_desert_32bpp.png",
    "tropical_groundtiles_deserttransition": "tropical_groundtiles_deserttransition_32bpp.png",
    "tropical_groundtiles_snowtransition": "tropical_groundtiles_snowtransition_32bpp.png",
    "temperate_groundtiles": "temperate_groundtiles_32bpp.png",
    "temperate_groundtiles_rocks": "temperate_groundtiles_rocks_32bpp.png",
    "temperate_groundtiles_rocks_alt": "temperate_groundtiles_rocks_alt_32bpp.png",
    "temperate_groundtiles_rough": "temperate_groundtiles_rough_32bpp.png",
    "temperate_groundtiles_deserttransition": "temperate_groundtiles_deserttransition_32bpp.png",
    "temperate_groundtiles_snowtransition": "temperate_groundtiles_snowtransition_32bpp.png",
    "toyland_groundtiles": "toyland_groundtiles_32bpp.png",
    "toyland_groundtiles_rocks": "toyland_groundtiles_rocks_32bpp.png",
    "toyland_groundtiles_rough": "toyland_groundtiles_rough_32bpp.png",
    "toyland_shoretiles": "toyland_shoretiles_32bpp.png",
    "toyland_yellowtiles": "toyland_yellowtiles_32bpp.png"
  }

  gridline_opacity_normal = 15/255
  gridline_overlay_overlay = 55/255

  # Dithering borders of terrain tiles for smoothing of slopes
  do_dithering = False
  dither_range = 4

  print("Running in scale "+str(scale)+" (tile size "+str(tile_size)+")")
  for terrain_key in terrain_list:
    repeat_y = 48
    if terrain_key == "farm_groundtiles":
      repeat_y += 1 # hacked, because of off by one pixel error in 'stacking' 64px field sprites
    print("  "+terrain_key)
    terrain_image_path = os.path.join(base_path, terrain_list[terrain_key])
    gridline_overlay_path = os.path.join(base_path, "groundtiles_gridlines.png")
    output_grid_path = os.path.join(base_path, "pygen", terrain_key+"_gridline_32bpp.png")
    output_nogrid_path = os.path.join(base_path, "pygen", terrain_key+"_nogridline_32bpp.png")
    if check_update_needed([__file__, terrain_image_path, gridline_overlay_path], output_grid_path):
      print("  ", "Generating", os.path.basename(output_grid_path))
      terrain_image = Image.open(terrain_image_path).convert("RGB")
      # Smooth/dither top edges
      if "toyland" not in terrain_key and do_dithering == True:
        terrain_image_smooth = terrain_image.copy()
        for x in range(0, terrain_image_smooth.width):
          for y in range(0, terrain_image_smooth.height):
              for d in range(0, dither_range * scale):
                if y + d < terrain_image_smooth.height:
                  if terrain_image_smooth.getpixel((x, y)) == (0, 0, 255):
                    if uniform(0, 1) < 1/(dither_range * scale):
                      v = terrain_image_smooth.getpixel((x, y + d))
                      if v != (0, 0, 255) and v != (255, 255, 255):
                        terrain_image_smooth.putpixel((x, y), v)
        terrain_image_smooth.save(output_nogrid_path)
      else:
        terrain_image.save(output_nogrid_path)
      # Overlay gridlines
      target_w, target_h = terrain_image.size
      target_image = terrain_image.crop((0, 0, target_w, target_h)).convert("RGBA")
      gridline_image = Image.open(gridline_overlay_path).convert("RGBA")
      gridline_overlay = target_image.copy()
      for i in range(0, int(target_h / (repeat_y * scale)) + 1):
        gridline_overlay = paste_to(gridline_image, 0, 0, target_w / scale, repeat_y, gridline_overlay, 0, i * repeat_y, scale)
      target_image = blendmode_overlay(target_image, gridline_overlay, gridline_opacity_normal, "normal")
      target_image = blendmode_overlay(target_image, gridline_overlay, gridline_overlay_overlay, "overlay")
      # Save
      target_image.save(output_grid_path)
    else:
      print("  ", "Skipped", os.path.basename(output_grid_path))

if __name__ == "__main__":
  if len(sys.argv) < 2:
    terrain_gridoverlay(int(sys.argv[1]))
  else:
    terrain_gridoverlay(int(sys.argv[1]), sys.argv[2])
