#!/usr/bin/env python3

# building_shapeproc.py
# Generates output images used for dithering to 8bpp
# Inputs (should be of same dimensions for each group):
#   *_base_shape.png (8bpp, OpenTTD palette)
#    Encodes key ground textures with specific colours
#    Encodes wall/foliage/woodwork shape with specific colours for specific wall directions and materials
#    Encodes recolouring information (per column of sprites) in pixel colours on row 0
#   *_base_overlayshading.png (RGBA)
#    Overlay for shading, used as opacity 0.25 overlay mode overlay
#  *_base_overlaynormal.png (RGBA, should use only OpenTTD palette colours)
#    Overlay for overdrawn pixel art, used as opacity 1.0 normal mode overlay
# Resources:
#  textures
#    Images in ../textures relative to working directory
#    Should tile
# Outputs:
#  *_base_32bpp.png (RGB)
#    Recoloured and textured shape image, including overlays
#  *_base_palmask.png (8bpp, OpenTTD palette)
#    Recoloured shape image, overlaid with _overlaynormal
#    Used for restricting colour ranges during dithering

# Run in directory with images to process
# python3 building_shapeproc.py <scale>
#   scale: 1 or 4
#    64px or 256px tiles respective
#    Defines shading scheme and textures to use

# Dependencies
# pip3 install pillow
# pip3 install numpy
# pip3 install blend-modes

from PIL import Image
from PIL import ImageFilter
from random import randint
import numpy, blend_modes # For overlay blending
import glob, os, sys

from tools import openttd_palettise, check_update_needed, openttd_palette_image, palette_image, openttd_palette, openttd_palette_animated, openttd_palette_generalmask

def buildings_baseshapeproc(scale, climate, snow, base_path, verbose=True):
  print("Building base", base_path)
  if os.path.isdir(os.path.join(base_path)) == False: os.mkdir(os.path.join(base_path))
  if os.path.isdir(os.path.join(base_path, "pygen")) == False: os.mkdir(os.path.join(base_path, "pygen"))

  namesuffix = ""
  if snow:
    print("Using snow! (or desert)")
    namesuffix = "snow_"

  # make toyland sprites in parallel
  if climate == "toyland":
    namesuffix += "toyland_"

  # OpenTTD DOS palette, RGB values
  palette_r = openttd_palette["r"]
  palette_g = openttd_palette["g"]
  palette_b = openttd_palette["b"]
  # Setup palette image, used for applying palette quickly
  palimage=openttd_palette_image()

  # Special palette details
  # Values to exclude during dithering
  palette_exclude = openttd_palette_animated + openttd_palette_generalmask
  palette_generalmask = openttd_palette_generalmask


  # ==Insets or outsets a blurred version masked indices==
  #image_32bit: RGB image to modify
  #image_shape, indices: indexed shape reference image
  #indices: indices in shape image to modify, either inset within these indices or outset around these indices
  #offset_x, offset_y: distance to shift blurred inset in x and y
  #blur, value, opacity: blur radius, value (colour) and opacity of blurred inset
  #blend: "normal" or "overlay"
  #mode: "inset" or "outset"
  def inout_blur(image_32bit, image_shape, indices, offset_x, offset_y, blur, value, opacity, blend, mode):
    # Make black image for merging channels
    image_black = Image.new("L", (image_32bit.size), 0)
    image_white = Image.new("L", (image_32bit.size), 255)
    image_value_r = Image.new("L", (image_32bit.size), value[0])
    image_value_g = Image.new("L", (image_32bit.size), value[1])
    image_value_b = Image.new("L", (image_32bit.size), value[2])
    # Make sharp mask from indices (white = in indices)
    if mode == "inset":
      v = [255] * 256
      for i in range(len(indices)):
        v[indices[i]] = 0
    elif mode == "outset":
      v = [0] * 256
      index_exclude = palette_exclude + indices
      for i in range(len(index_exclude)):
        v[index_exclude[i]] = 255
    mask_palimg = palette_image(v, v, v)
    image_shape.putpalette(mask_palimg.getpalette())
    image_mask = image_shape.convert("L")
    # Make blurred overlay (black = in indices, with spatial offset)
    if mode == "inset":
      v = [255] * 256
      for i in range(len(indices)):
        v[indices[i]] = 0
    elif mode == "outset":
      v = [0] * 256
      for i in range(len(indices)):
        v[indices[i]] = 255
    mask_palimg = palette_image(v, v, v)
    image_shape.putpalette(mask_palimg.getpalette())
    image_overlay = Image.new("L", (image_mask.size))
    image_overlay.paste(image_shape, (offset_x, offset_y))
    image_overlay = image_overlay.filter(ImageFilter.GaussianBlur(radius=blur))
    image_overlay = Image.merge("RGBA", (image_value_r, image_value_g, image_value_b, image_overlay))
    # Mask blurred overlay with sharp mask
    image_transparent = Image.merge("RGBA", (image_black, image_black, image_black, image_black))
    image_overlay.paste(image_transparent, (0, 0), image_mask)
    # Overlay blurred image
    r, g, b = image_32bit.convert("RGB").split()
    image_32bit = Image.merge("RGBA", (r, g, b, image_white))
    image_bg_arr = numpy.array(image_32bit).astype(float)
    image_fg_arr = numpy.array(image_overlay).astype(float)
    if blend == "overlay":
      image_blended_arr_float = blend_modes.overlay(image_bg_arr, image_fg_arr, opacity)
    elif blend == "normal":
      image_blended_arr_float = blend_modes.normal(image_bg_arr, image_fg_arr, opacity)
    image_blended_arr = numpy.uint8(image_blended_arr_float)
    image_out = Image.fromarray(image_blended_arr)
    return image_out

  def overlay_texture(image_32bit, image_shape, image_texture, indices, opacity, blend):
    # Make black image for merging channels
    image_black = Image.new("L", (image_32bit.size), 0)
    image_white = Image.new("L", (image_32bit.size), 255)
    # Make sharp mask from indices (white = in indices)
    v = [255] * 256
    for i in range(len(indices)):
      v[indices[i]] = 0
    mask_palimg = palette_image(v, v, v)
    image_shape.putpalette(mask_palimg.getpalette())
    image_mask = image_shape.convert("L")
    image_width, image_height = image_32bit.size
    # Make texture large enough for overlay
    image_overlay = Image.new("RGBA", (image_32bit.size))
    texture_width, texture_height = image_texture.size
    for x in range(int(image_width/texture_width)+1):
      for y in range(int(image_height/texture_height)+1):
        image_overlay.paste(image_texture, (x * texture_width, y * texture_height))
    # Mask blurred overlay with sharp mask
    image_transparent = Image.merge("RGBA", (image_black, image_black, image_black, image_black))
    image_overlay.paste(image_transparent, (0, 0), image_mask)
    # Overlay texture image
    r, g, b = image_32bit.convert("RGB").split()
    image_32bit = Image.merge("RGBA", (r, g, b, image_white))
    image_bg_arr = numpy.array(image_32bit).astype(float)
    image_fg_arr = numpy.array(image_overlay).astype(float)
    if blend == "overlay":
      image_blended_arr_float = blend_modes.overlay(image_bg_arr, image_fg_arr, opacity)
    elif blend == "normal":
      image_blended_arr_float = blend_modes.normal(image_bg_arr, image_fg_arr, opacity)
    image_blended_arr = numpy.uint8(image_blended_arr_float)
    image_out = Image.fromarray(image_blended_arr)
    return image_out

  def simple_overlay_texture(image_32bit, image_shape, image_texture, indices):
    # Make black image for merging channels
    image_black = Image.new("L", (image_32bit.size), 0)
    image_white = Image.new("L", (image_32bit.size), 255)
    # Make sharp mask from indices (white = in indices)
    v = [0] * 255
    for i in range(len(indices)):
      v[indices[i]] = 255
    mask_palimg = palette_image(v, v, v)
    image_shape.putpalette(mask_palimg.getpalette())
    image_mask = image_shape.convert("L")
    image_width, image_height = image_32bit.size
    # Make texture large enough for overlay
    image_texture = image_texture.convert("RGBA")
    image_overlay = Image.new("RGBA", (image_32bit.size))
    texture_width, texture_height = image_texture.size
    for x in range(int(image_width/texture_width)+1):
      for y in range(int(image_height/texture_height)+1):
        image_overlay.paste(image_texture, (x * texture_width, y * texture_height))
    # Mask texture overlay with sharp mask
    # Overlay texture image
    image_32bit.paste(image_overlay, (0, 0), image_mask)
    return image_32bit
  
  def open_texture(base_path, texture_name, scale):
    scale_specific_path = os.path.join(base_path, "../../textures", str(scale*64), texture_name+".png")
    general_path = os.path.join(base_path, "../../textures", texture_name+".png")
    if os.path.exists(scale_specific_path):
      return Image.open(scale_specific_path).convert("RGBA")
    elif os.path.exists(general_path):
      return Image.open(general_path).convert("RGBA")

  # ==Adds value noise to masked indices==
  #image_32bit: RGB image to modify
  #image_shape, indices: indexed shape reference image and indices to use
  #power: +/- value range to add to value channel
  def add_value_noise(image_32bit, image_shape, indices, power):
    image_hsv = image_32bit.convert("HSV");
    h, s, v = image_hsv.split()
    width, height = image_32bit.size
    for x in range(width):
      for y in range(height):
        if image_shape.getpixel((x, y)) in indices:
          v.putpixel((x, y), v.getpixel((x, y)) + randint(-power, power))
    image_hsv = Image.merge("HSV", (h, s, v))
    image_32bit = image_hsv.convert("RGB")
    return image_32bit

  suffix = "_base_shape.png";
  index_frame = [15, 255] #### HACKED!!! Why does index conversion of input sprite not use index 255/white? ####
  # Input image must be forrectly formatted:
  # Sprites must be organised in with a 1px white (index index_frame) border
  # Sprites must be organised in columns, each column will be recoloured together
  # Pixels on the first row, aligned with the start of the sprite column, indicate remapping
  # Source indices for remapping:
  # Base area (1 entry), walls main (3 entries), walls alt (3), roof (3), windows (3), woodwork (3), metalwork (3)
  index_groundtextures = [82, 107, 8, 3]
  index_remaps = [1, 41, 42, 43, 90, 91, 92, 115, 116, 117]
  index_remaps_snow = [-1, -1, -1, 211, -1, -1, 211, -1, -1, 211]
  index_base = [1]
  index_walls = [41, 42, 43]
  index_greenery = [90, 91, 92]
  index_woodwork = [115, 116, 117]
  for input_file in glob.glob(os.path.join(base_path, "*"+suffix)):
    input_name = os.path.basename(input_file)
    print(" %s in scale %d mode" % (input_name, scale))
    # check for input file changes
    normal_overlay_name = input_file[:-len(suffix)]+"_base_overlaynormal.png"
    alpha_overlay_name = input_file[:-len(suffix)]+"_base_overlayalpha.png"
    shading_overlay_name = input_file[:-len(suffix)]+"_base_overlayshading.png"
    climatename = ""
    if climate == "toyland":
      climatename = "toyland_"
    image_unshaded_name = os.path.join(base_path, "pygen", input_name[:-len(suffix)]+"_"+namesuffix+"base_palmask.png")
    image_shaded_name = os.path.join(base_path, "pygen", input_name[:-len(suffix)]+"_"+namesuffix+"base_32bpp.png")
    if check_update_needed([__file__, input_file, normal_overlay_name, alpha_overlay_name, shading_overlay_name] + glob.glob(os.path.join(base_path, "../../textures/*.png")) + glob.glob(os.path.join(base_path, "../../textures/*/*.png")), image_shaded_name):
      print("  ", "Generating", os.path.basename(image_shaded_name))
      with Image.open(input_file) as image:
        # Open shape image
        width, height = image.size
        # Convert shape image to OpenTTD 8 bit
        image_shape = openttd_palettise(image)
        # Apply colouring specified by pixel above each column of sprites
        # Loop through _second_ row of pixels (multiplied by scale)
        image_colorised = Image.new("P", (image_shape.size))
        image_colorised.paste(image_shape, (0,0))
        image_colorised.putpalette(image_shape.getpalette())
        x = 0
        while x < width - scale:
          # Find start of a sprite
          while x < width - scale and image_shape.getpixel((x, 2 * scale)) in index_frame:
            x += 1
          # Find sprite width
          w = 0
          while x + w < width - scale and image_shape.getpixel((x + w, 2 * scale)) not in index_frame:
            w += 1
          if verbose == True:
            print(" Sprite column, x: %d, w: %d" % (x, w))
          # Lookup color remapping
          if w > len(index_remaps):
            # Only process if sprite column is wide enough to have all remapping info in row 1
            index_target = []
            for i in range(len(index_remaps)):
              index_target.append(image_shape.getpixel((x + i * scale, 0 * scale)))
            if verbose == True:
              print("  Source indices: "+",".join(map(str, index_remaps)))
              print("  Target indices: "+",".join(map(str, index_target)))
            # Apply new colours
            current_r = palette_r.copy()
            current_g = palette_g.copy()
            current_b = palette_b.copy()
            for i in range(len(index_remaps)):
              current_r[index_remaps[i]] = palette_r[index_target[i]]
              current_g[index_remaps[i]] = palette_g[index_target[i]]
              current_b[index_remaps[i]] = palette_b[index_target[i]]
            # Override with snow colors, if in snow mode
            if snow == True:
              #Replace horizontal and roofs with snow colours
              for i in range(len(index_remaps_snow)):
                if index_remaps_snow[i] != -1:
                  current_r[index_remaps[i]] = palette_r[index_remaps_snow[i]]
                  current_g[index_remaps[i]] = palette_g[index_remaps_snow[i]]
                  current_b[index_remaps[i]] = palette_b[index_remaps_snow[i]]
            current_palimg = palette_image(current_r, current_g, current_b)
            current_spriteset = image_colorised.crop((x, 0, x + w, height))
            current_spriteset.putpalette(current_palimg.getpalette())
            current_spriteset = openttd_palettise(current_spriteset)
            image_colorised.paste(current_spriteset, (x, 0))
            # Increment x position by width for the next sprite set
            x += w
        # Make copy of the image for shading
        image_32bit = Image.new("RGB", (image_colorised.size))
        image_32bit.paste(image_colorised, (0, 0))
        # Save a copy of the unshaded image, with the pixel art overlay if it exists, as the palette mask
        image_unshaded = Image.new("P", (image_colorised.size))
        image_unshaded.paste(image_colorised, (0, 0))
        image_unshaded.putpalette(image_colorised.getpalette())
        # Set pixels in ground texture to background colour (ie. allow all colours for dithering)
        for x in range(width):
          for y in range(height):
            if image_shape.getpixel((x, y)) in index_groundtextures:
              image_unshaded.putpixel((x, y), 0)
        if os.path.isfile(normal_overlay_name):
          image_unshaded = overlay_texture(image_32bit, image_shape, Image.open(normal_overlay_name), range(256), 255/255, "normal")
        image_unshaded.save(image_unshaded_name, "PNG")
        # Shade using standard rules
        # Ground textures
        texture_opacity = 255
        if snow == True:
          image_32bit = simple_overlay_texture(image_32bit, image_shape, open_texture(base_path, "ground_alt_arctic", scale), [index_groundtextures[0]])
        elif climate == "temperate":
          image_32bit = simple_overlay_texture(image_32bit, image_shape, open_texture(base_path, "ground_grass_temperate", scale), [index_groundtextures[0]])
        elif climate == "arctic":
          image_32bit = simple_overlay_texture(image_32bit, image_shape, open_texture(base_path, "ground_grass_arctic", scale), [index_groundtextures[0]])
        elif climate == "tropical":
          image_32bit = simple_overlay_texture(image_32bit, image_shape, open_texture(base_path, "ground_grass_tropical", scale), [index_groundtextures[0]])
        elif climate == "tropicaldesert":
          image_32bit = simple_overlay_texture(image_32bit, image_shape, open_texture(base_path, "ground_alt_tropical", scale), [index_groundtextures[0]])
        else:
          image_32bit = simple_overlay_texture(image_32bit, image_shape, open_texture(base_path, "ground_grass_temperate", scale), [index_groundtextures[0]])
        image_32bit = simple_overlay_texture(image_32bit, image_shape, open_texture(base_path, "ground_bare", scale), [index_groundtextures[1]])
        image_32bit = simple_overlay_texture(image_32bit, image_shape, open_texture(base_path, "ground_concrete", scale), [index_groundtextures[2]])
        image_32bit = simple_overlay_texture(image_32bit, image_shape, open_texture(base_path, "ground_tarmac", scale), [index_groundtextures[3]])
        # Greenery noise and shading
        if scale == 1:
          image_32bit = add_value_noise(image_32bit, image_shape, index_greenery, 27)
        elif scale == 4:
          image_32bit = overlay_texture(image_32bit, image_shape, open_texture(base_path, "foliage", scale), index_greenery, 92/255, "overlay")
        image_32bit = inout_blur(image_32bit, image_shape, index_greenery, 1, -1, 2, (0, 0, 0), 191/255, "overlay", "inset")
        image_32bit = inout_blur(image_32bit, image_shape, index_greenery, -1, 1, 2, (255, 255, 255), 191/255, "overlay", "inset")
        # Wall noise and shading
        image_32bit = add_value_noise(image_32bit, image_shape, index_walls, 15)
        image_32bit = inout_blur(image_32bit, image_shape, index_walls, 1, -1, 1, (0, 0, 0), 191/255, "overlay", "inset")
        image_32bit = inout_blur(image_32bit, image_shape, index_walls, -1, 1, 1, (255, 255, 255), 191/255, "overlay", "inset")
        # Blurred ground overlay
        image_32bit = inout_blur(image_32bit, image_shape, [index_groundtextures[0], 0, 255], -2, 0, 1.5, (255, 255, 255), 159/255, "overlay", "inset")
        image_32bit = inout_blur(image_32bit, image_shape, [index_groundtextures[0], index_groundtextures[1], 0, 255], 0, 0, 1.5, (0, 0, 0), 159/255, "overlay", "inset")
        image_32bit = inout_blur(image_32bit, image_shape, [index_groundtextures[3], 0, 255], 2, 0, 1.5, (0, 0, 0), 159/255, "overlay", "inset")
        # Building base shadow
        image_32bit = inout_blur(image_32bit, image_shape, index_base, -2, 0, 1.5, (0, 0, 0), 191/255, "normal", "outset")
        # Add manual overlays, if the files exist
        # Overlay overlay_alpha, if it exists
        if os.path.isfile(alpha_overlay_name):
          image_32bit = image_32bit.convert("RGBA")
          image_32bit = Image.alpha_composite(image_32bit, Image.open(alpha_overlay_name).convert("RGBA"))
        # Shading/overlay mode overlay
        if os.path.isfile(shading_overlay_name):
          image_32bit = overlay_texture(image_32bit, image_shape, Image.open(shading_overlay_name), range(256), 63/255, "overlay")
        # Pixel art/normal mode overlay
        if os.path.isfile(normal_overlay_name):
          image_32bit = overlay_texture(image_32bit, image_shape, Image.open(normal_overlay_name), range(256), 255/255, "normal")
        # Save shaded image
        image_32bit.save(image_shaded_name, "PNG")
    else:
      print("  ", "Skipping", os.path.basename(image_shaded_name))

if __name__ == "__main__":
  snow = False
  if sys.argv[3].lower() == "true":
    snow = True
  if len(sys.argv) < 3:
    buildings_baseshapeproc(sys.argv[1], sys.argv[2], snow, ".")
  else:
    buildings_baseshapeproc(sys.argv[1], sys.argv[2], snow, sys.argv[4])
