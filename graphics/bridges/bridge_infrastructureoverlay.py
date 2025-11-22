#!/usr/bin/env python3

from PIL import Image
import os, sys

from tools import check_update_needed, paste_to, overlay_bluetransp, mask_image, openttd_palettise

def infrastructure_bridge_infrastructureoverlay(scale, mode, base_path=".", verbose=True):
  print(base_path)
  if os.path.isdir(os.path.join(base_path)) == False: os.mkdir(os.path.join(base_path))
  if os.path.isdir(os.path.join(base_path, "pygen")) == False: os.mkdir(os.path.join(base_path, "pygen"))

  tile_size = scale * 64

  if mode == "bridges" or mode == "bridges_toyland":
    # Source tile positions in infrastructure
    tile_positions = [
      [1, 1, 64, 32],
      [66, 1, 64, 32],
    ]
    # vertical offset for infrastructure tiles
    v_offs = [81, 81]
    if mode == "bridges":
      # Infrastructure sprites to use
      infrastructure_list = {
        "road": "road_general_bridge_32bpp.png",
        "rail": "rail_general_bridge_32bpp.png",
        "monorail": "monorail_general_bridge_32bpp.png",
        "maglev": "maglev_general_bridge_32bpp.png"
      }
      # Bridge sprites to use
      bridge_list = {
        "template": "bridge_template_32bpp.png",
        "deckonly": "bridge_deckonly_32bpp.png",
        "steelfast": "bridge_steelfast_32bpp.png",
        "steelslow": "bridge_steelslow_32bpp.png",
        "wood": "bridge_wood_32bpp.png",
        "girder": "bridge_girder_32bpp.png",
        "suspension": "bridge_suspension_32bpp.png",
        "tubular": "bridge_tubular_32bpp.png"
      }
    elif mode == "bridges_toyland":
      # Infrastructure sprites to use
      infrastructure_list = {
        "road": "road_toyland_bridge_32bpp.png",
        "rail": "rail_toyland_bridge_32bpp.png",
        "monorail": "monorail_toyland_bridge_32bpp.png",
        "maglev": "maglev_toyland_bridge_32bpp.png"
      }
      # Bridge sprites to use
      bridge_list = {
        "template_toyland": "bridge_template_32bpp.png",
        "deckonly_toyland": "bridge_deckonly_32bpp.png",
        "steelfast_toyland": "bridge_steelfast_toyland_32bpp.png",
        "steelslow_toyland": "bridge_steelslow_toyland_32bpp.png",
        "wood_toyland": "bridge_wood_toyland_32bpp.png",
        "girder_toyland": "bridge_girder_toyland_32bpp.png",
        "suspension_toyland": "bridge_suspension_toyland_32bpp.png",
        "tubular_toyland": "bridge_tubular_toyland_32bpp.png"
      }
    bridgemask = "bridge_deckmask.png"
    composite_over = True
  elif mode == "railramps" or mode == "roadramps" or mode == "railramps_toyland" or mode == "roadramps_toyland":
    # Source tile positions in infrastructure
    if mode == "railramps" or mode == "railramps_toyland":
      tile_positions = [
        [66, 1, 64, 32],
        [66, 1, 64, 32],
        [1, 1, 64, 32],
        [1, 1, 64, 32],
        [1301, 1, 64, 39],
        [1431, 1, 64, 23],
        [1496, 1, 64, 39],
        [1366, 1, 64, 23]
      ]
      # Infrastructure sprites to use
      if mode == "railramps":
        infrastructure_list = {
          "rail": "rail_general_bridge_32bpp.png",
          "monorail": "monorail_general_bridge_32bpp.png",
          "maglev": "maglev_general_bridge_32bpp.png"
        }
      elif mode == "railramps_toyland":
        infrastructure_list = {
          "rail": "rail_toyland_bridge_32bpp.png",
          "monorail": "monorail_toyland_bridge_32bpp.png",
          "maglev": "maglev_toyland_bridge_32bpp.png"
        }
    elif mode == "roadramps" or mode == "roadramps_toyland":
      # Tile poisitions
      tile_positions = [
        [66, 1, 64, 32],
        [66, 1, 64, 32],
        [1, 1, 64, 32],
        [1, 1, 64, 32],
        [976, 1, 64, 39],
        [1106, 1, 64, 23],
        [1171, 1, 64, 39],
        [1041, 1, 64, 23]
      ]
      # Infrastructure sprites to use
      if mode == "roadramps":
        infrastructure_list = {
          "road": "road_general_bridge_32bpp.png"
        }
      elif mode == "roadramps_toyland":
        infrastructure_list = {
          "road": "road_toyland_bridge_32bpp.png"
        }
    # vertical offset for infrastructure tiles
    v_offs = [16, 24, 16, 24, 16, 24, 16, 24]
    # Terrain sprites to use
    if mode == "roadramps" or mode == "railramps":
      bridge_list = {
        "ramps_general": "bridgeramps_general_32bpp.png",
        "ramps_norecolour": "bridgeramps_norecolour_32bpp.png",
        "ramps_wood": "bridgeramps_wood_32bpp.png",
        "ramps_deckonly": "bridgeramps_deckonly_32bpp.png",
      }
    elif mode == "roadramps_toyland" or mode == "railramps_toyland":
      bridge_list = {
        "ramps_general_toyland": "bridgeramps_general_toyland_32bpp.png",
        "ramps_norecolour_toyland": "bridgeramps_norecolour_32bpp.png",
        "ramps_wood_toyland": "bridgeramps_wood_toyland_32bpp.png",
        "ramps_deckonly_toyland": "bridgeramps_deckonly_32bpp.png",
      }
    bridgemask = "bridgeramps_deckmask.png"
    composite_over = False

  print("Running in scale "+str(scale)+" (tile size "+str(tile_size)+") "+mode+" mode")
  for bridge_key in bridge_list:
    print(" "+bridge_key)
    for infrastructure_key in infrastructure_list:
      print("  "+infrastructure_key)
      # input image paths
      bridge_image_path = os.path.join(base_path, bridge_list[bridge_key])
      bridgemask_image_path = os.path.join(base_path, bridgemask)
      infrastructure_image_path = os.path.join(base_path, "..", "..", "infrastructure", str(tile_size), "pygen", infrastructure_list[infrastructure_key])
      bridge_palmask_path = bridge_list[bridge_key][:-len("_32bpp.png")]+"_palmask.png"
      image_output_path = os.path.join(base_path, "pygen", bridge_key+"_"+infrastructure_key+"_32bpp.png")
      palmask_output_path = os.path.join(base_path, "pygen", bridge_key+"_"+infrastructure_key+"_palmask.png")
      # main image
      if check_update_needed([__file__, bridge_image_path, bridgemask_image_path, infrastructure_image_path], image_output_path):
        print("  ", "Generating", os.path.basename(image_output_path))
        # if update is needed
        # Open bridge image
        bridge_image = Image.open(bridge_image_path)
        # Open bridge image
        bridgemask_image = Image.open(bridgemask_image_path)
        # Make images containing arranged infrastructure sprites and arranged mask sprites
        infrastructure_image = Image.open(infrastructure_image_path)
        infrastructure_target_image = Image.new("RGBA", bridge_image.size, (255, 255, 255, 255))
        mask_target_image = Image.new("RGBA", bridge_image.size, (255, 255, 255, 255))
        for i in range(int((bridge_image.size[0] - 1) / (tile_size + 1))):
          infrastructure_target_image = paste_to(infrastructure_image, tile_positions[i % len(tile_positions)][0], tile_positions[i % len(tile_positions)][1], tile_positions[i % len(tile_positions)][2], tile_positions[i % len(tile_positions)][3], infrastructure_target_image, i * (tile_size // scale + 1) + 1, 1 + v_offs[i % len(tile_positions)], scale)
          mask_target_image = paste_to(bridgemask_image, 1 + (i % len(tile_positions)) * (tile_size // scale + 1), 0, tile_size, bridge_image.size[1], mask_target_image, i * (tile_size // scale + 1) + 1, 0, scale)
        target_image = mask_image(infrastructure_target_image, mask_target_image)
        # Overlay for 32bpp image
        if composite_over:
          target_image = overlay_bluetransp(bridge_image, target_image)
        else:
          target_image = overlay_bluetransp(target_image, bridge_image)
        # Save 32bpp image
        target_image.save(image_output_path)
      else:
        print("  ", "Skipped", os.path.basename(image_output_path))
      # palmask image
      if check_update_needed([__file__, bridge_palmask_path], palmask_output_path):
        print("  ", "Generating", os.path.basename(palmask_output_path))
        # if update is needed
        # Load palmask image, if it exists
        if os.path.isfile(bridge_palmask_path):
          bridge_image_palmask = Image.open(bridge_palmask_path)
          bridge_image_palmask = openttd_palettise(bridge_image_palmask)
          bridge_image_palmask.save(palmask_output_path)
      else:
        print("  ", "Skipping", os.path.basename(palmask_output_path))

if __name__ == "__main__":
  if len(sys.argv) < 3:
    infrastructure_bridge_infrastructureoverlay(int(sys.argv[1]), sys.argv[2])
  else:
    infrastructure_bridge_infrastructureoverlay(int(sys.argv[1]), sys.argv[2], sys.argv[3])
