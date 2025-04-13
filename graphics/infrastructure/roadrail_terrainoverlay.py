#!/usr/bin/env python3

from PIL import Image
import os, sys

from tools import check_update_needed, blend_overlay, paste_to

def infrastructure_roadrail_terrainoverlay(scale, mode, base_path=".", verbose=True):
  print("Road/Rail", base_path)
  if os.path.isdir(os.path.join(base_path)) == False: os.mkdir(os.path.join(base_path))
  if os.path.isdir(os.path.join(base_path, "pygen")) == False: os.mkdir(os.path.join(base_path, "pygen"))

  tile_size = scale * 64

  if mode == "rail" or mode == "rail_toyland":
    # Remapping of tile positions
    tile_positions = [
      [1, 1, 64, 32],
      [1, 1, 64, 32],
      [1, 1, 64, 32],
      [1, 1, 64, 32],
      [1, 1, 64, 32],
      [1, 1, 64, 32],
      [1, 1, 64, 32],
      [1, 1, 64, 32],
      [1, 1, 64, 32],
      [1, 1, 64, 32],
      [1, 1, 64, 32],
      [1, 1, 64, 32],
      [639, 1, 64, 41],
      [321, 1, 64, 32],
      [81, 1, 64, 32],
      [161, 1, 64, 24],
      [1119, 1, 64, 32],
      [559, 1, 64, 24],
      [879, 1, 64, 32],
      [1039, 1, 64, 41],
      [959, 1, 64, 41],
      [479, 1, 64, 24],
      [241, 1, 64, 24],
      [719, 1, 64, 41],
      [1, 1, 64, 32],
      [1, 1, 64, 32]
    ]
    if mode == "rail_toyland":
      infrastructure_list = {
        "rail": "rail_toyland",
        "monorail": "monorail_toyland",
        "maglev": "maglev_toyland"
      }
      terrain_list = {
        "toyland_grass": os.path.join("pygen", "toyland_groundtiles_gridline_32bpp.png"),
        "toyland_alt_grass": os.path.join("pygen", "toyland_alt_groundtiles_gridline_32bpp.png"),
        "toyland_grass_nogridline": os.path.join("pygen", "toyland_groundtiles_nogridline_32bpp.png"),
        "toyland_alt_grass_nogridline": os.path.join("pygen", "toyland_alt_groundtiles_nogridline_32bpp.png"),
        "toyland_concrete": "toyland_concretetiles_32bpp.png",
        "toyland_bridge": "general_bridgetiles_32bpp.png"
      }
    else:
      # Infrastructure sprites to use
      infrastructure_list = {
        "rail": "rail",
        "monorail": "monorail",
        "maglev": "maglev"
      }
      # Terrain sprites to use
      terrain_list = {
        "arctic_grass": os.path.join("pygen", "arctic_groundtiles_gridline_32bpp.png"),
        "arctic_snow": os.path.join("pygen", "arctic_groundtiles_snow_gridline_32bpp.png"),
        "tropical_grass": os.path.join("pygen", "tropical_groundtiles_gridline_32bpp.png"),
        "tropical_desert": os.path.join("pygen", "tropical_groundtiles_desert_gridline_32bpp.png"),
        "temperate_grass": os.path.join("pygen", "temperate_groundtiles_gridline_32bpp.png"),
        "arctic_grass_nogridline": os.path.join("pygen", "arctic_groundtiles_nogridline_32bpp.png"),
        "arctic_snow_nogridline": os.path.join("pygen", "arctic_groundtiles_snow_nogridline_32bpp.png"),
        "tropical_grass_nogridline": os.path.join("pygen", "tropical_groundtiles_nogridline_32bpp.png"),
        "tropical_desert_nogridline": os.path.join("pygen", "tropical_groundtiles_desert_nogridline_32bpp.png"),
        "temperate_grass_nogridline": os.path.join("pygen", "temperate_groundtiles_nogridline_32bpp.png"),
        "general_concrete": "general_concretetiles_32bpp.png",
        "general_bridge": "general_bridgetiles_32bpp.png"
      }
  elif mode == "road" or mode == "road_noline" or mode == "road_toyland":
    tile_positions = [
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [959, 1, 65, 41],
      [479, 1, 65, 24],
      [241, 1, 65, 24],
      [719, 1, 65, 41]
    ]
    if mode == "road":
      # Infrastructure sprites to use
      infrastructure_list = {
        "road": "road",
      }
      # Terrain sprites to use
      terrain_list = {
        "arctic_grass": os.path.join("pygen", "arctic_groundtiles_gridline_32bpp.png"),
        "arctic_snow": os.path.join("pygen", "arctic_groundtiles_snow_gridline_32bpp.png"),
        "temperate_grass": os.path.join("pygen", "temperate_groundtiles_gridline_32bpp.png"),
        "arctic_grass_nogridline": os.path.join("pygen", "arctic_groundtiles_nogridline_32bpp.png"),
        "arctic_snow_nogridline": os.path.join("pygen", "arctic_groundtiles_snow_nogridline_32bpp.png"),
        "temperate_grass_nogridline": os.path.join("pygen", "temperate_groundtiles_nogridline_32bpp.png"),
        "arctic_desert": os.path.join("pygen", "tropical_groundtiles_desert_gridline_32bpp.png"),
        "arctic_desert_nogridline": os.path.join("pygen", "tropical_groundtiles_desert_nogridline_32bpp.png"),
        "general_bridge": "general_bridgetiles_32bpp.png",
      }
    if mode == "road_noline":
      # Infrastructure sprites to use
      infrastructure_list = {
        "road": "road_noline",
      }
      # Terrain sprites to use
      terrain_list = {
        "tropical_grass": os.path.join("pygen", "tropical_groundtiles_gridline_32bpp.png"),
        "tropical_desert": os.path.join("pygen", "tropical_groundtiles_desert_gridline_32bpp.png"),
        "tropical_grass_nogridline": os.path.join("pygen", "tropical_groundtiles_nogridline_32bpp.png"),
        "tropical_desert_nogridline": os.path.join("pygen", "tropical_groundtiles_desert_nogridline_32bpp.png"),
        "tropical_snow": os.path.join("pygen", "arctic_groundtiles_snow_gridline_32bpp.png"),
        "tropical_snow_nogridline": os.path.join("pygen", "arctic_groundtiles_snow_nogridline_32bpp.png"),
      }
    if mode == "road_toyland":
      # Infrastructure sprites to use
      infrastructure_list = {
        "road": "road_toyland",
      }
      # Terrain sprites to use
      terrain_list = {
        "toyland_grass": os.path.join("pygen", "toyland_groundtiles_gridline_32bpp.png"),
        "toyland_alt_grass": os.path.join("pygen", "toyland_alt_groundtiles_gridline_32bpp.png"),
        "toyland_grass_nogridline": os.path.join("pygen", "toyland_groundtiles_nogridline_32bpp.png"),
        "toyland_alt_grass_nogridline": os.path.join("pygen", "toyland_alt_groundtiles_nogridline_32bpp.png"),
        "toyland_bridge": "general_bridgetiles_32bpp.png"
      }
  elif mode == "road_town" or mode == "road_town_toyland":
    # Includes bus stops
    tile_positions = [
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [959, 1, 65, 41],
      [479, 1, 65, 24],
      [241, 1, 65, 24],
      [719, 1, 65, 41],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32],
      [1, 1, 65, 32]
    ]
    if mode == "road_town_toyland":
      infrastructure_list = {
        "road": "road_toyland"
      }
      terrain_list = {
        "toyland_concrete": "toyland_concretetiles_32bpp.png"
      }
    else:
      infrastructure_list = {
        "road": "road_town"
      }
      terrain_list = {
        "general_concrete": "general_concretetiles_32bpp.png"
      }
  elif mode == "airport_modern":
    # Remapping of tile positions
    tile_positions = [
      [1, 1, 64, 32]
    ] * 25
    # Infrastructure sprites to use
    infrastructure_list = {
      "airport_modern": "airport_modern",
      "airport_old": "airport_old"
    }
    # Terrain sprites to use
    terrain_list = {
      "arctic_grass": os.path.join("pygen", "arctic_groundtiles_gridline_32bpp.png"),
      "arctic_snow": os.path.join("pygen", "arctic_groundtiles_snow_gridline_32bpp.png"),
      "tropical_grass": os.path.join("pygen", "tropical_groundtiles_gridline_32bpp.png"),
      "tropical_desert": os.path.join("pygen", "tropical_groundtiles_desert_gridline_32bpp.png"),
      "temperate_grass": os.path.join("pygen", "temperate_groundtiles_gridline_32bpp.png"),
      "toyland_grass": os.path.join("pygen", "toyland_groundtiles_gridline_32bpp.png"),
      "toyland_alt_grass": os.path.join("pygen", "toyland_alt_groundtiles_gridline_32bpp.png"),
      "arctic_grass_nogridline": os.path.join("pygen", "arctic_groundtiles_nogridline_32bpp.png"),
      "arctic_snow_nogridline": os.path.join("pygen", "arctic_groundtiles_snow_nogridline_32bpp.png"),
      "tropical_grass_nogridline": os.path.join("pygen", "tropical_groundtiles_nogridline_32bpp.png"),
      "tropical_desert_nogridline": os.path.join("pygen", "tropical_groundtiles_desert_nogridline_32bpp.png"),
      "temperate_grass_nogridline": os.path.join("pygen", "temperate_groundtiles_nogridline_32bpp.png"),
      "toyland_grass_nogridline": os.path.join("pygen", "toyland_groundtiles_nogridline_32bpp.png"),
      "toyland_alt_grass_nogridline": os.path.join("pygen", "toyland_alt_groundtiles_nogridline_32bpp.png")
    }

  # Output image properties
  output_width = (scale + (tile_size + scale) * len(tile_positions))
  output_height = 0
  for i in range(len(tile_positions)):
    if tile_positions[i][3] * scale + scale > output_height:
      output_height = tile_positions[i][3] * scale + scale

  print("Running in scale "+str(scale)+" (tile size "+str(tile_size)+") "+mode+" mode")
  for terrain_key in terrain_list:
    print(" "+terrain_key)
    # Make image containing arranged terrain backgrounds
    terrain_image_path = os.path.join(base_path, "..", "..", "terrain", str(tile_size), terrain_list[terrain_key])
    terrain_image = Image.open(terrain_image_path)
    target_image = Image.new("RGBA", (output_width, output_height), (255, 255, 255, 255))
    for i in range(len(tile_positions)):
      target_image = paste_to(terrain_image, tile_positions[i][0], tile_positions[i][1], tile_positions[i][2], tile_positions[i][3], target_image, i * (tile_size // scale + 1) + 1, 1, scale)
    target_image_width, target_image_height = target_image.size
    # Make a palmask image from infrastructure background palmask images, if it exists, othwise pure blue
    terrain_palmask_path = os.path.join(base_path, "..", "..", "terrain", str(tile_size), terrain_list[terrain_key][:len("_32bpp.png")]+"_palmask.png")
    if os.path.isfile(terrain_palmask_path):
      terrain_image_palmask = Image.open(terrain_palmask_path)
      target_image_palmask = Image.new("P", (output_width, output_height), 255)
      target_image_palmask.putpalette(palimg.getpalette())
      for i in range(len(tile_positions)):
        target_image_palmask = paste_to(terrain_image_palmask, tile_positions[i][0], tile_positions[i][1], tile_positions[i][2], tile_positions[i][3], target_image_palmask,i * (tile_size // scale + 1) + 1, 1, scale)
    else:
        target_image_palmask = Image.new("RGBA", (output_width, output_height), (0, 0, 255, 255))
    for infrastructure_key in infrastructure_list:
      # Check if update needed
      name_overlayalpha = os.path.join(base_path, infrastructure_list[infrastructure_key]+"_overlayalpha.png")
      name_overlayalpha2 = os.path.join(base_path, infrastructure_list[infrastructure_key]+"_overlayalpha2.png")
      name_overlayshading = os.path.join(base_path, infrastructure_list[infrastructure_key]+"_overlayshading.png")
      name_overlaynormal = os.path.join(base_path, infrastructure_list[infrastructure_key]+"_overlaynormal.png")
      output_normal_path = os.path.join(base_path, "pygen", infrastructure_key+"_"+terrain_key+"_32bpp.png")
      output_palmask_path = os.path.join(base_path, "pygen", infrastructure_key+"_"+terrain_key+"_palmask.png")
      if check_update_needed([__file__, terrain_image_path, name_overlayalpha, name_overlayalpha2, name_overlayshading, name_overlaynormal], output_normal_path):
        print("  ", "Generating", os.path.basename(output_normal_path))
        # Overlay each infrastructure set
        print("  "+infrastructure_key)
        output_image = target_image.copy()
        # Overlay overlay_alpha, if it exists
        if os.path.isfile(name_overlayalpha):
          infrastructure_image = Image.open(name_overlayalpha).convert("RGBA")
          infrastructure_image = infrastructure_image.crop((0, 0, target_image_width, target_image_height))
          output_image = Image.alpha_composite(output_image, infrastructure_image)
        # Overlay additional overlay, if it exists
        if os.path.isfile(name_overlayalpha2):
          infrastructure_image = Image.open(name_overlayalpha2).convert("RGBA")
          infrastructure_image = infrastructure_image.crop((0, 0, target_image_width, target_image_height))
          output_image = Image.alpha_composite(output_image, infrastructure_image)
        # Overlay overlayshading, if it exists
        if os.path.isfile(name_overlayshading):
          infrastructure_image = Image.open(name_overlayshading).convert("RGBA")
          infrastructure_image = infrastructure_image.crop((0, 0, target_image_width, target_image_height))
          output_image = blend_overlay(output_image, infrastructure_image, 192/255)
        # Save 32bpp image
        output_image.save(output_normal_path)
        # Make and save palmask image
        # Overlay infrastructure normal overlay, if it exists
        if os.path.isfile(name_overlaynormal):
          infrastructure_image = Image.open(name_overlaynormal).convert("RGBA")
          target_image_palmask = Image.alpha_composite(target_image_palmask, infrastructure_image)
        # If either exists, then save
        if os.path.isfile(terrain_palmask_path) or os.path.isfile(name_overlaynormal):
          target_image_palmask.save(output_palmask_path)
      else:
        print("  ", "Skipped", os.path.basename(output_normal_path))

if __name__ == "__main__":
  if len(sys.argv) < 3:
    infrastructure_roadrail_terrainoverlay(int(sys.argv[1]), sys.argv[2])
  else:
    infrastructure_roadrail_terrainoverlay(int(sys.argv[1]), sys.argv[2], sys.argv[3])
