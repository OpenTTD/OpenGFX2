#!/usr/bin/env python3

from PIL import Image
import skimage, numpy
import glob, os, sys
import random

from tools import openttd_palettise, check_update_needed, openttd_palette, openttd_palette_animated, openttd_palette_generalmask, openttd_color_set_start, openttd_color_set_length, openttd_palette_image, palette_image

# Primary conversion function
# dither_factor is the additional multiplicative factor on error diffusion, use between 0 and 1
# src and pal are the image to dither and an image defining palette restrictions
def make_8bpp(src32bpp, palmask):
  # Setup palette image, used for applying palette quickly
  palimage=openttd_palette_image()

  if palmask is None:
    palmask = Image.new("P", (src32bpp.size), 0)
    palmask.putpalette(palimage.getpalette())

  # 'Normal' palette entries, everything expect action colours and pure white (index 255)
  colors_normal = [x for x in range(255) if x not in openttd_palette_animated]

  # Start by making sure the images are the correct mode
  # Source must be RGBA
  src32bpp = src32bpp.convert("RGBA")
  # Palette must be 8-bit with OpenTTD palette
  palmask = openttd_palettise(palmask)

  # Dither function
  # Do dithering in RGB space
  # Do not dither (propagate pixel value errors) to indices in openttd_palette_animated or openttd_palette_generalmask
  # If palmask pixel index is in one of the color sets, restrict dithering to only indices in that set
  def make_dithered(src32bpp, palmask, dither_factor=1, max_error_propagation=16, dither_mode="sierra_lite"):
    # Find colour groups in palmask image and make an image recording the color set per pixel
    # If sets pixel is not 255 then dithering is restricted to indices in color_set[pixel value]

    def most_similar_in_palette(pr, pg, pb):
      dist = 255 * 255 * 255
      index = 0
      for i in colors_normal:
        cd = (pr - openttd_palette["r"][i]) * (pr - openttd_palette["r"][i]) + (pg - openttd_palette["g"][i]) * (pg - openttd_palette["g"][i]) + (pb - openttd_palette["b"][i]) * (pb - openttd_palette["b"][i])
        if cd < dist:
          dist = cd
          index = i
      return index

    def most_similar_in_color_set(pr, pg, pb, color_set):
      dist = 255 * 255 * 255
      index = 0
      start_index = openttd_color_set_start[color_set]
      end_index = start_index + openttd_color_set_length[color_set]
      for i in range(start_index, end_index):
        cd = (pr - openttd_palette["r"][i]) * (pr - openttd_palette["r"][i]) + (pg - openttd_palette["g"][i]) * (pg - openttd_palette["g"][i]) + (pb - openttd_palette["b"][i]) * (pb - openttd_palette["b"][i])
        if cd < dist:
          dist = cd
          index = i
      return index

    v = [255] * 256
    for i in range(len(openttd_color_set_start)):
      for j in range(openttd_color_set_length[i]):
        v[openttd_color_set_start[i] + j] = i
    sets_palimg = palette_image(v, v, v)
    sets = palmask.copy()
    sets.putpalette(sets_palimg.getpalette())
    sets = sets.convert("L")
    
    # Find pixels in src32bpp exactly matching openttd_palette_generalmask and make an image with this mask
    # Do not propagate pixel value errors through donotdither pixels with value 255
    width, height = src32bpp.size
    donotdither = Image.new("L", (width, height), 0)
    for x in range(width):
      for y in range(height):
        pr, pg, pb, pa = src32bpp.getpixel((x, y))
        for i in range(len(openttd_palette_generalmask)):
          if openttd_palette["r"][openttd_palette_generalmask[i]] == pr and openttd_palette["g"][openttd_palette_generalmask[i]] == pg and openttd_palette["b"][openttd_palette_generalmask[i]] == pb:
            donotdither.putpixel((x, y), 255)
            break
    
    # Dither settings
    if dither_mode == "sierra":
      # Sierra http://www.tannerhelland.com/4660/dithering-eleven-algorithms-source-code/
      dox = 2
      doy = 0
      df = 32
      da = [
        [-1, -1, -1,  5,  3],
        [ 2,  4,  5,  4,  2],
        [ 0,  2,  3,  2,  0]
      ]
    elif dither_mode == "sierra_lite":
      # Sierra lite http://www.tannerhelland.com/4660/dithering-eleven-algorithms-source-code/
      dox = 1
      doy = 0
      df = 4
      da = [
        [-1, -1,  2],
        [ 1,  1,  0]
      ]

    def do_dithering_noalpha():
      # Dither, without trying to do anything clever with alpha
      res8bpp = Image.new("P", (src32bpp.size))
      res8bpp.putpalette(palimage.getpalette())
      for y in range(height):
        for x in range(width):
          pr, pg, pb = src32bpp.getpixel((x, y))
          if pr == 0 and pg == 0 and pb == 255:
            # Fast processing of pure blue pixels
            res8bpp.putpixel((x, y), 0)
          elif donotdither.getpixel((x, y)) == 255:
            # Do not dither this pixel, just set nearest value
            res8bpp.putpixel((x, y), most_similar_in_palette(pr, pg, pb))
          else:
            # Dither this pixel
            if sets.getpixel((x, y)) != 255:
              # Dither this pixel within a color set
              res8bpp.putpixel((x, y), most_similar_in_color_set(pr, pg, pb, sets.getpixel((x, y))))
            else:
              # Dither this pixel to any color
              res8bpp.putpixel((x, y), most_similar_in_palette(pr, pg, pb))
            # Diffuse errors according to the dithering matrix
            error = [0, 0, 0]
            error[0] = pr - openttd_palette["r"][res8bpp.getpixel((x, y))]
            error[1] = pg - openttd_palette["g"][res8bpp.getpixel((x, y))]
            error[2] = pb - openttd_palette["b"][res8bpp.getpixel((x, y))]
            # Do error propagation
            for b in range(len(da)):
              for a in range(len(da[0])):
                # For each x and y offset a and b in dither array
                if da[b][a] != -1 and x + a < width - 1 and y + b < height - 1:
                  # If a valid dither value and within image bounds
                  if donotdither.getpixel((x, y)) != 255:
                    # Do not propagate errors through pixels identified as donotdither
                    # Alter pixel value to propagate errors
                    pcr, pcg, pcb = src32bpp.getpixel((x + a - dox, y + b - doy))
                    pcr = int(pcr + error[0] * dither_factor * da[b][a] / df)
                    pcg = int(pcg + error[1] * dither_factor * da[b][a] / df)
                    pcb = int(pcb + error[2] * dither_factor * da[b][a] / df)
                    src32bpp.putpixel((x + a - dox, y + b - doy), (pcr, pcg, pcb))
                    # Clamp propagated error to a maximum of 16 per channel
                    error = [min(error[0], max_error_propagation), min(error[1], max_error_propagation), min(error[2], max_error_propagation)]
      # Return result
      return res8bpp
    
    def do_dithering_alpha():
      # Dither, converting alpha to dithered transparent blue
      res8bpp = Image.new("P", (src32bpp.size))
      res8bpp.putpalette(palimage.getpalette())
      for y in range(height):
        for x in range(width):
          pr, pg, pb, pa = src32bpp.getpixel((x, y))
          if pa == 0 or (pr == 0 and pg == 0 and pb == 255):
            # Fast processing of pure transparent and pure blue pixels
            res8bpp.putpixel((x, y), 0)
          elif donotdither.getpixel((x, y)) == 255:
            # Do not dither this pixel, just set nearest value, randomised based on alpha
            if pa / 255 < 0.5:
              res8bpp.putpixel((x, y), 0)
            else:
              res8bpp.putpixel((x, y), most_similar_in_palette(pr, pg, pb))
          else:
            # Dither this pixel
            if sets.getpixel((x, y)) != 255:
              # Dither this pixel within a color set
              outindex = most_similar_in_color_set(pr, pg, pb, sets.getpixel((x, y)))
            else:
              # Dither this pixel to any color
              outindex = most_similar_in_palette(pr, pg, pb)
            # Diffuse errors according to the dithering matrix
            if pa / 255 > 0.5:
              res8bpp.putpixel((x, y), outindex)
              error = [0, 0, 0, 0]
              error[0] = pr - openttd_palette["r"][res8bpp.getpixel((x, y))]
              error[1] = pg - openttd_palette["g"][res8bpp.getpixel((x, y))]
              error[2] = pb - openttd_palette["b"][res8bpp.getpixel((x, y))]
              error[3] = pa - 255
            else:
              res8bpp.putpixel((x, y), 0)
              error = [0, 0, 0, pa]
            # Do error propagation
            for b in range(len(da)):
              for a in range(len(da[0])):
                # For each x and y offset a and b in dither array
                if da[b][a] != -1 and x + a < width - 1 and y + b < height - 1:
                  # If a valid dither value and within image bounds
                  if donotdither.getpixel((x, y)) != 255:
                    # Do not propagate errors through pixels identified as donotdither
                    # Alter pixel value to propagate errors
                    pcr, pcg, pcb, pca = src32bpp.getpixel((x + a - dox, y + b - doy))
                    pcr = int(pcr + error[0] * dither_factor * da[b][a] / df)
                    pcg = int(pcg + error[1] * dither_factor * da[b][a] / df)
                    pcb = int(pcb + error[2] * dither_factor * da[b][a] / df)
                    pca = int(pca + error[3] * dither_factor * da[b][a] / df)
                    src32bpp.putpixel((x + a - dox, y + b - doy), (pcr, pcg, pcb, pca))
                    # Clamp propagated error to a maximum of 16 per channel
                    error = [min(error[0], max_error_propagation), min(error[1], max_error_propagation), min(error[2], max_error_propagation), min(error[3], max_error_propagation)]
      # Return result
      return res8bpp
    
    # Check if there is an alpha channel
    if has_alpha(src32bpp):
      return do_dithering_alpha()
    else:
      src32bpp = src32bpp.convert("RGB")
      return do_dithering_noalpha()
  
  # Convert src32bpp to 8-bit with OpenTTD palette using custom dithering
  # Dithers in HSV space, restricting colour sets when specified in palmask
  dithered = make_dithered(src32bpp, palmask)
  
  # Overlay pixels in palmask exactly matching indices in openttd_palette_animated over dithered image
  # Mask from indices
  v = [0] * 255
  for i in range(len(openttd_palette_animated)):
    v[openttd_palette_animated[i]] = 255
  mask_palimg = palette_image(v, v, v)
  mask = palmask.copy()
  mask.putpalette(mask_palimg.getpalette())
  mask = mask.convert("L")
  # Paste using mask
  dithered.paste(palmask, (0, 0), mask)
  
  # Return result
  return dithered

def make_white_transp(src32bit):
  """
  Uses pure blue pixels from a 32bit image as an alpha mask, making a 32bpp image with blue pixels as transparent.
  """
  if has_alpha(src32bit):
    # If input image already has an alpha channel, just use that
    return src32bit
  # Otherwise, make an alpha channel using magic blue pixels for transparency
  # Handle input image as numpy array, working in RGB
  src32bit = numpy.array(src32bit.convert("RGB").split())
  # Alpha mask from where 32bit image is (0, 0, 255) blue
  out32bitalpha = numpy.where((src32bit[0] == 0) & (src32bit[1] == 0) & (src32bit[2] == 255), 0, 255).astype(numpy.uint8)
  # Make RGBA composite
  return Image.merge("RGBA", (Image.fromarray(src32bit[0]), Image.fromarray(src32bit[1]), Image.fromarray(src32bit[2]), Image.fromarray(out32bitalpha)))

def make_32bpp_remainder(src8bit, src32bit):
  """
  Uses a input 32bit image and its 8bit pallete conversion to make 32bpp (but grayscale) map of brightness remainder.
  Makes an output 32bit image which, when used with the input 8bit image as a mask, inherits hue/sat from 8bit but brightness from input 32bpp.
  """
  # Handle input images as numpy arrays, working in RGB
  src8bit = numpy.array(src8bit.convert("RGB").split())
  src32bit = numpy.array(src32bit.convert("RGB").split())
  # Alpha mask from where 8bit image is (0, 0, 255) blue
  out32bitalpha = numpy.where((src8bit[0] == 0) & (src8bit[1] == 0) & (src8bit[2] == 255), 0, 255).astype(numpy.uint8)
  # Brightness remainder from value of 32bit image minus value of 8bit image
  out32bitvalue = (numpy.max(src32bit, axis=0) - numpy.max(src8bit, axis=0) + 128).astype(numpy.uint8)
  # Combine brightness remainder with alpha mask for output
  return Image.merge("RGBA", (Image.fromarray(out32bitvalue), Image.fromarray(out32bitvalue), Image.fromarray(out32bitvalue), Image.fromarray(out32bitalpha)))

def find_sprites(src32bit):
  """
  Find sprites within a 32bpp spritesheet. Assumes sprite background is (255, 255, 255). Identifies sprites as bounding rectangles of non-(255, 255, 255) areas.
  Returns a list of (x, y, x+w, y+h) bounds per sprite.
  """
  # Handle input image as numpy array, working in RGB
  src32bit = numpy.array(src32bit.convert("RGB").split())
  # Mask pure white regions to black, everything else to white
  mask = numpy.where((src32bit[0] == 255) & (src32bit[1] == 255) & (src32bit[2] == 255), 0, 255).astype(numpy.uint8)
  # use skimage to find the objects (sprites)
  lab = skimage.measure.label(mask)
  table = skimage.measure.regionprops_table(lab, mask, properties=("bbox", "area_bbox"))
  # parse and return (swapped x and y in skimage)
  sprites = []
  for i in range(len(table["bbox-0"])):
    sprites.append([table["bbox-1"][i], table["bbox-0"][i], table["bbox-3"][i], table["bbox-2"][i]])
  return sprites

def has_alpha(src32bit):
  """
  Check if a 32bpp image has an alpha channel.
  """
  r, g, b, a = src32bit.convert("RGBA").split()
  a = numpy.array(a)
  return a.min() != 255

def make_output_parallel_handler(input=input):
  """
  Worker function for make_output_parallel
  """
  # input is: image, palmask, dither factor, x, y
  image_8bpp = make_8bpp(input[0], input[1])
  image_bt32bpp = make_white_transp(input[0])
  image_rm32bpp = make_32bpp_remainder(image_8bpp, image_bt32bpp)
  return [image_8bpp, image_bt32bpp, image_rm32bpp, input[2], input[3]]

def make_output_parallel(image, palmask):
  """
  Dither a 32bpp image, outputting 8bpp images.
  Uses multiprocessing to parallelize the dithering process of sprites within the spritesheet.
  """
  import concurrent, multiprocessing
  from tqdm.auto import tqdm
  sprites = find_sprites(image)
  #setup worklist by cropping sprites from input image
  worklist = []
  for i in range(len(sprites)):
    # each entry is: image, palmask, x, y
    if palmask is not None:
      worklist.append([image.crop((sprites[i][0], sprites[i][1], sprites[i][2], sprites[i][3])), palmask.crop((sprites[i][0], sprites[i][1], sprites[i][2], sprites[i][3])), sprites[i][0], sprites[i][1]])
    else:
      worklist.append([image.crop((sprites[i][0], sprites[i][1], sprites[i][2], sprites[i][3])), None, sprites[i][0], sprites[i][1]])
  #setup workers based on multiprocess mode
  multiprocess_mode = "process" # process seems to give easily the highest performance
  workers = multiprocessing.cpu_count()
  if multiprocess_mode is None:
    Executor = concurrent.futures.ThreadPoolExecutor
    workers = 1
  elif multiprocess_mode == "process":
    Executor = concurrent.futures.ProcessPoolExecutor
  elif multiprocess_mode == "thread":
    Executor = concurrent.futures.ThreadPoolExecutor
  #process
  with Executor(workers) as executor:
    futures = [executor.submit(make_output_parallel_handler, input=input) for input in worklist]
    results = [future.result() for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), smoothing=0)]
  #recombine cropped sprites into spritesheets
  image_8bpp = Image.new("P", (image.size), 255)
  image_8bpp.putpalette(results[0][0].getpalette())
  image_bt32bpp = Image.new("RGBA", (image.size), (255, 255, 255, 255))
  image_rm32bpp = Image.new("RGBA", (image.size), (255, 255, 255))
  for i in range(len(results)):
    image_8bpp.paste(results[i][0], (results[i][3], results[i][4]))
    image_bt32bpp.paste(results[i][1], (results[i][3], results[i][4]))
    image_rm32bpp.paste(results[i][2], (results[i][3], results[i][4]))
  return image_8bpp, image_bt32bpp, image_rm32bpp

def make_output(image, palmask):
  """
  Dither a 32bpp image, outputting 8bpp images.
  """
  image_8bpp = make_8bpp(image, palmask);
  image_bt32bpp = make_white_transp(image)
  image_rm32bpp = make_32bpp_remainder(image_8bpp, image_bt32bpp)
  return image_8bpp, image_bt32bpp, image_rm32bpp

def custom_dither_file(input_file, suffix="_32bpp.png", verbose=True):
  """
  Dither a single image file, outputting 8bpp images.
  Only process images lacking a *_8bpp output _or_ sources/dependencies more recently than the *_8bpp output
  """
  name = input_file[:-len(suffix)]
  if check_update_needed([__file__, input_file, name+"_palmask.png"], name+"_8bpp.png"):
    if verbose == True:
      print("  ", "Converting", os.path.basename(input_file))
    with Image.open(input_file) as image:
      if os.path.isfile(name+"_palmask.png"):
        palmask = Image.open(name+"_palmask.png")
      else:
        palmask = None
      image_8bpp, image_bt32bpp, image_rm32bpp = make_output_parallel(image, palmask)
      #image_8bpp, image_bt32bpp, image_rm32bpp = make_output(image, palmask)
      image_8bpp.save(name+"_8bpp.png", "PNG")
      image_bt32bpp.save(name+"_bt32bpp.png", "PNG")
      image_rm32bpp.save(name+"_rm32bpp.png", "PNG")
  else:
    if verbose == True:
      print("  ", "Skipping", os.path.basename(input_file))

def custom_dither_directory(input_directory, suffix="_32bpp.png", verbose=True):
  """
  Dither all images in a directory with a given suffix, outputting 8bpp images.
  """
  if verbose == True:
    print("Dithering directory", input_directory)
  for input_file in glob.glob(os.path.join(input_directory, "*"+suffix)):
    custom_dither_file(input_file, suffix=suffix, verbose=verbose)

if __name__ == '__main__':
  if len(sys.argv) < 2:
    custom_dither_directory(".")
  else:
    custom_dither_directory(sys.argv[1])
