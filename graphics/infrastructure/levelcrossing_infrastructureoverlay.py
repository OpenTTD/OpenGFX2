#!/usr/bin/env python3

from PIL import Image
import os, sys

from tools import check_update_needed, alpha_to, paste_to

def infrastructure_levelcrossing_infrastructureoverlay(scale, base_path=".", verbose=True):
  print("Level crossing", base_path)
  if os.path.isdir(os.path.join(base_path)) == False: os.mkdir(os.path.join(base_path))
  if os.path.isdir(os.path.join(base_path, "pygen")) == False: os.mkdir(os.path.join(base_path, "pygen"))

  tile_size = scale * 64

  # Road tiles to use
  road_tile_positions = [
    [66, 1, 64, 32],
    [1, 1, 64, 32],
    [66, 1, 64, 32],
    [1, 1, 64, 32]
  ]
  # Rail tiles to use
  rail_tile_positions = [
    [1, 1, 64, 32],
    [66, 1, 64, 32],
    [1, 1, 64, 32],
    [66, 1, 64, 32]
  ]
  # Rail types to use
  infrastructure_list = {
    "rail": "rail",
    "monorail": "monorail",
    "maglev": "maglev"
  }
  # Terrain types to use
  terrain_list = {
    "arctic_grass": "arctic_grass",
    "arctic_snow": "arctic_snow",
    "tropical_grass": "tropical_grass",
    "tropical_desert": "tropical_desert",
    "temperate_grass": "temperate_grass",
    "toyland_grass": "toyland_grass",
    "toyland_alt_grass": "toyland_alt_grass",
    "concrete": "general_concrete",
    "toyland_concrete": "toyland_concrete",
    "arctic_grass_nogridline": "arctic_grass_nogridline",
    "arctic_snow_nogridline": "arctic_snow_nogridline",
    "tropical_grass_nogridline": "tropical_grass_nogridline",
    "tropical_desert_nogridline": "tropical_desert_nogridline",
    "temperate_grass_nogridline": "temperate_grass_nogridline",
    "toyland_grass_nogridline": "toyland_grass_nogridline",
    "toyland_alt_grass_nogridline": "toyland_alt_grass_nogridline",
  }

  # Output image properties
  output_width = (scale + (tile_size + scale) * len(rail_tile_positions))
  output_height = 0
  for i in range(len(rail_tile_positions)):
    if rail_tile_positions[i][3] + 1 > output_height:
      output_height = rail_tile_positions[i][3] + 1
  output_height += 1
  output_height *= scale

  print("Running in scale "+str(scale)+" (tile size "+str(tile_size)+")")
  for terrain_key in terrain_list:
    print(" "+terrain_key)
    for infrastructure_key in infrastructure_list:
      print("  "+infrastructure_key)
      # Check if update needed
      terrain_image_path = os.path.join(base_path, "pygen", infrastructure_list[infrastructure_key]+"_"+terrain_list[terrain_key]+"_32bpp.png")
      road_image_path = os.path.join(base_path, "road_overlayalpha.png")
      if "toyland" in terrain_key:
        road_image_path = os.path.join(base_path, "road_toyland_overlayalpha.png")
      if "toyland" in terrain_key:
        overlay_alpha_path = os.path.join(base_path, "toyland_" + infrastructure_list[infrastructure_key]+"_levelcrossing_overlayalpha.png")
      else:
        overlay_alpha_path = os.path.join(base_path, infrastructure_list[infrastructure_key]+"_levelcrossing_overlayalpha.png")
      overlay_normal_path = os.path.join(base_path, "levelcrossing_overlaynormal.png")
      output_normal_path = os.path.join(base_path, "pygen", "levelcrossing_road_"+infrastructure_key+"_"+terrain_key+"_32bpp.png")
      output_palmask_path = os.path.join(base_path, "pygen", "levelcrossing_road_"+infrastructure_key+"_"+terrain_key+"_palmask.png")
      if check_update_needed([__file__, terrain_image_path, road_image_path, overlay_alpha_path, overlay_normal_path], output_normal_path):
        print("  ", "Generating", os.path.basename(output_normal_path))
        # Make image containing arranged rail background tiles
        terrain_image = Image.open(terrain_image_path).convert("RGBA")
        target_image = Image.new("RGBA", (output_width, output_height))
        for i in range(len(rail_tile_positions)):
          target_image = paste_to(terrain_image, rail_tile_positions[i][0], rail_tile_positions[i][1], rail_tile_positions[i][2], rail_tile_positions[i][3], target_image, i * (tile_size // scale + 1) + 1, 1, scale)
        # Overlay road overlayalpha
        road_image = Image.open(road_image_path).convert("RGBA")
        for i in range(len(road_tile_positions)):
          target_image = alpha_to(road_image, road_tile_positions[i][0], road_tile_positions[i][1], road_tile_positions[i][2], road_tile_positions[i][3], target_image, i * (tile_size // scale + 1) + 1, 1, scale)
        # Overlay overlayalpha
        infrastructure_alpha = Image.open(overlay_alpha_path).convert("RGBA")
        target_image = Image.alpha_composite(target_image, infrastructure_alpha)
        # Overlay crossing lights
        infrastructure_normal = Image.open(overlay_normal_path).convert("RGBA")
        target_image = Image.alpha_composite(target_image, infrastructure_normal)
        target_image.save(output_normal_path)
        # Save palmask image
        blank_palmask = Image.new("RGBA", (output_width, output_height), (0, 0, 255))
        infrastructure_normal = Image.alpha_composite(blank_palmask, infrastructure_normal)
        infrastructure_normal.save(output_palmask_path)
      else:
        print("  ", "Skipped", os.path.basename(output_normal_path))

if __name__ == "__main__":
  if len(sys.argv) < 3:
    infrastructure_levelcrossing_infrastructureoverlay(int(sys.argv[1]), sys.argv[2])
  else:
    infrastructure_levelcrossing_infrastructureoverlay(int(sys.argv[1]), sys.argv[2], sys.argv[3])
