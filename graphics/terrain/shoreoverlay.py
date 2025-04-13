#!/usr/bin/env python3

from PIL import Image
import os, sys

from tools import openttd_palettise, palette_image, openttd_palette_image, check_update_needed, blend_overlay

def terrain_shoreoverlay(scale, mode, base_path=".", verbose=True):
  print("Shores", base_path)
  if os.path.isdir(os.path.join(base_path)) == False: os.mkdir(os.path.join(base_path))
  if os.path.isdir(os.path.join(base_path, "pygen")) == False: os.mkdir(os.path.join(base_path, "pygen"))

  tile_size = scale * 64

  if mode == "normal":
    # Terrain sprites to use
    terrain_list = {
      "arctic_grass_gridline": os.path.join("pygen", "arctic_groundtiles_gridline_32bpp.png"),
      "arctic_snow_gridline": os.path.join("pygen", "arctic_groundtiles_snow_gridline_32bpp.png"),
      "tropical_grass_gridline": os.path.join("pygen", "tropical_groundtiles_gridline_32bpp.png"),
      "tropical_desert_gridline": os.path.join("pygen", "tropical_groundtiles_desert_gridline_32bpp.png"),
      "temperate_grass_gridline": os.path.join("pygen", "temperate_groundtiles_gridline_32bpp.png"),
      "general_concrete": "general_concretetiles_32bpp.png",
      "arctic_grass_nogridline": os.path.join("pygen", "arctic_groundtiles_nogridline_32bpp.png"),
      "arctic_snow_nogridline": os.path.join("pygen", "arctic_groundtiles_snow_nogridline_32bpp.png"),
      "tropical_grass_nogridline": os.path.join("pygen", "tropical_groundtiles_nogridline_32bpp.png"),
      "tropical_desert_nogridline": os.path.join("pygen", "tropical_groundtiles_desert_nogridline_32bpp.png"),
      "temperate_grass_nogridline": os.path.join("pygen", "temperate_groundtiles_nogridline_32bpp.png")
    }
    shoreline_overlay_path = "shorelines_overlaynormal.png"
  elif mode == "toyland":
    terrain_list = {
      "toyland_grass_gridline": os.path.join("pygen", "toyland_shoretiles_gridline_32bpp.png"),
      "toyland_grass_nogridline": os.path.join("pygen", "toyland_shoretiles_nogridline_32bpp.png"),
      "toyland_alt_grass_gridline": os.path.join("pygen", "toyland_alt_shoretiles_gridline_32bpp.png"),
      "toyland_alt_grass_nogridline": os.path.join("pygen", "toyland_alt_shoretiles_nogridline_32bpp.png"),
    }
    shoreline_overlay_path = "shorelines_toyland_overlaynormal.png"

  print("Running in scale "+str(scale)+" (tile size "+str(tile_size)+")")
  for terrain_key in terrain_list:
    print("  "+terrain_key)
    terrain_image_path = os.path.join(base_path, terrain_list[terrain_key])
    shoreline_shading_path = os.path.join(base_path, "shorelines_overlayshading.png")
    output_main_path = os.path.join(base_path, "pygen", terrain_key+"_shoretiles_palmask.png")
    output_palmask_path = os.path.join(base_path, "pygen", terrain_key+"_shoretiles_32bpp.png")
    shoreline_overlay_path = os.path.join(base_path, shoreline_overlay_path)
    if check_update_needed([__file__, terrain_image_path, shoreline_overlay_path, shoreline_shading_path], output_main_path):
      print("  ", "Generating", os.path.basename(output_main_path))
      terrain_image = Image.open(terrain_image_path).convert("RGB")
      shore_image = Image.open(shoreline_overlay_path)
      shore_image = openttd_palettise(shore_image)
      width, height = shore_image.size
      target_image = terrain_image.crop((0, 0, width, height))
      # Save shore_image as palmask image
      shore_image.save(os.path.join(base_path, "pygen", terrain_key+"_shoretiles_palmask.png"))
      # Overlay shading, if it exists
      target_image = target_image.convert("RGBA")
      if os.path.isfile("shorelines_overlayshading.png") and mode == "normal":
        print("shorelines_overlayshading.png")
        shoreline_shading = Image.open("shorelines_overlayshading.png").convert("RGBA")
        target_image = blend_overlay(target_image, shoreline_shading, 192/255)
      # Overlay shore_image onto target_image using blue as transparent
      v = [255] * 256
      v[0] = 0
      mask_palimg = palette_image(v, v, v)
      shore_mask = shore_image.copy()
      shore_mask.putpalette(mask_palimg.getpalette())
      shore_mask = shore_mask.convert("L")
      target_image.paste(shore_image, (0, 0), shore_mask)
      # Save
      target_image.save(os.path.join(base_path, "pygen", terrain_key+"_shoretiles_32bpp.png"))
    else:
      print("  ", "Skipping", os.path.basename(output_main_path))

if __name__ == "__main__":
  if len(sys.argv) < 3:
    terrain_shoreoverlay(int(sys.argv[1]), sys.argv[2])
  else:
    terrain_shoreoverlay(int(sys.argv[1]), sys.argv[2], sys.argv[3])
