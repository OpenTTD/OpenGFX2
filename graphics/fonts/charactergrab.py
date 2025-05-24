#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
from math import floor, ceil
import os
from tools import check_update_needed

def fonts_charactergrab(base_path):
  scales = [1, 2, 4]
  
  print("Font sprites", base_path)
  if os.path.isdir(os.path.join(base_path)) == False:
    os.mkdir(os.path.join(base_path))
  if os.path.isdir(os.path.join(base_path, "pygen")) == False:
    os.mkdir(os.path.join(base_path, "pygen"))
  for scale in scales:
    if os.path.isdir(os.path.join(base_path, str(scale))) == False:
      os.mkdir(os.path.join(base_path, str(scale)))
    if os.path.isdir(os.path.join(base_path, str(scale), "pygen")) == False:
      os.mkdir(os.path.join(base_path, str(scale), "pygen"))

  fonts = [
    {
      "name": "medium", # human readable name
      "code": "NORMAL", # name for NML font_glyph coding
      "mono": False, # monospace (force character width to equal space)
      "base": True, # base set font
      "basesetoffs": 2, # sprite number offset for base set
      "path": "openttd-ttf/openttd-sans/OpenTTD-Sans.ttf", # TTF path
      "size": 10, # font size for rendering
      "ascent": 8, # ascent (px at 1x)
      "descent": 2, # descent (px at 1x)
      "space": 3, # space width (px at 1x)
      "yoffs": 0, # vertical position for NML (will be multiplied by scale)
      "ydrawoffs": 0 # additional vertical offset (px) for drawing
    },
    {
      "name": "small",
      "code": "SMALL",
      "mono": False,
      "base": True,
      "basesetoffs": 226,
      "path": "openttd-ttf/openttd-small/OpenTTD-Small.ttf",
      "size": 6,
      "ascent": 6,
      "descent": 1,
      "space": 2,
      "yoffs": -1,
      "ydrawoffs": 0
    },
    {
      "name": "large",
      "code": "LARGE",
      "mono": False,
      "base": True,
      "basesetoffs": 450,
      "path": "openttd-ttf/openttd-serif/OpenTTD-Serif.ttf",
      "size": 18,
      "ascent": 16,
      "descent": 4,
      "space": 6,
      "yoffs": -1,
      "ydrawoffs": 2 # hack: top pixels can be lost, noticed for capitals with diacritics.
    },
    {
      "name": "mono",
      "code": "MONO",
      "mono": True,
      "base": False,
      "path": "openttd-ttf/openttd-mono/OpenTTD-Mono.ttf",
      "size": 10,
      "ascent": 8,
      "descent": 2,
      "space": 7,
      "yoffs": 0,
      "ydrawoffs": 0
    }
  ]

  # base charset uses private range for some symbols, these are used by the medium font and must be in the source ttf
  charsets = [
    {
      "name": "base",
      "path": "pygen/base-0002-font.pnml",
      "codemode": "block",
      "codesets": [
        {"start": 32, "end": 158},
        {"start": 376, "end": 376},
        {"start": 58016, "end": 58016},
        {"start": 161, "end": 169},
        {"start": 58026, "end": 58026},
        {"start": 171, "end": 171},
        {"start": 58028, "end": 58029},
        {"start": 174, "end": 174},
        {"start": 58031, "end": 58031},
        {"start": 176, "end": 179},
        {"start": 58036, "end": 58041},
        {"start": 186, "end": 187},
        {"start": 58044, "end": 58045},
        {"start": 190, "end": 255}
      ]
    },
    {
      "name": "extra",
      "path": "pygen/extra-chars.pnml",
      "codemode": "block",
      "codesets": [
        # Complete or targetedly complete blocks
        {"start": 32, "end": 126, "name": "Basic Latin"},
        {"start": 160, "end": 255, "name": "Latin-1 Supplement"},
        {"start": 256, "end": 383, "name": "Latin Extended-A"},
        {"start": 900, "end": 983, "name": "Greek, from Greek and Coptic"},
        {"start": 1024, "end": 1119, "name": "Cyrillic"},
        {"start": 8352, "end": 8383, "name": "Currency Symbols"},
        # Select additional characters
        # Latin
        {"start": 399, "end": 399}, # Latin Extended-B
        {"start": 401, "end": 402}, # Latin Extended-B
        {"start": 437, "end": 438}, # Latin Extended-B
        {"start": 536, "end": 539}, # Latin Extended-B
        {"start": 601, "end": 601}, # Latin Extended-B
        # Cyrillic
        {"start": 1168, "end": 1169}, # Cyrillic
        {"start": 1194, "end": 1195}, # Cyrillic
        {"start": 1232, "end": 1233}, # Cyrillic
        {"start": 1238, "end": 1239}, # Cyrillic
        {"start": 1266, "end": 1267}, # Cyrillic
        # Other
        {"start": 699, "end": 700}, # Diacritics
        {"start": 710, "end": 712}, # Diacritics
        {"start": 713, "end": 715}, # Diacritics
        {"start": 728, "end": 732}, # Diacritics
        {"start": 1423, "end": 1423}, # Currency
        {"start": 3647, "end": 3647}, # Currency
        {"start": 8208, "end": 8213}, # Punctuation
        {"start": 8216, "end": 8223}, # Punctuation
        {"start": 8230, "end": 8230}, # Punctuation
        {"start": 8249, "end": 8250}, # Punctuation
        {"start": 8470, "end": 8471}, # Letter-like symbols
        {"start": 8482, "end": 8482}, # Letter-like symbols
        {"start": 10216, "end": 10217}, # Mathematical symbols
        # Extended private use range
        {"start": 58013, "end": 58013},
      ]
    },
  ]

  # character codes which should be maximally cropped
  # hack: custom character range X (window close) icon should be maximally cropped
  cropcodes = [58029]

  defaultmaxwidthfactor = 2 # max glyph width, as a factor of font size
  outputpadding = 8
  outputcolumns = 32

  def get_glyph(font, scale, code):
    # setup shadow
    shadowoffset = 0
    if font["name"] == "medium":
      shadowoffset = 1
    # alignment hacks
    additionalstring = ""
    if font["name"] == "medium":
      additionalstring = "                i" # hack: characters can be one off in vertical direction unless forced with presence of i in the string.
    if font["name"] == "large":
      additionalstring = "                O" # hack: characters can be one off in vertical direction unless forced with presence of O (or other tall, rounded, character) in the string, noticed for eg. N vs O.
    # make output image and setup font
    image = Image.new("RGBA", (font["size"] * scale * maxwidthfactor, (font["ascent"] + font["descent"] + shadowoffset) * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.fontmode = "1" # aliased
    if font["name"] == "medium":
      draw.text((shadowoffset * scale, shadowoffset * scale + font["ydrawoffs"] * scale), chr(code) + additionalstring, font=font["imfont"], fill=(32, 32, 32, 255))
    draw.text((0, 0 + font["ydrawoffs"] * scale), chr(code) + additionalstring, font=font["imfont"], fill=(16, 16, 16, 255))
    imagebox = image.getbbox()
    if imagebox is None:
      # if no bounding box then no glyph
      if code == 32 or code == 160:
        # handle spaces
        imagebox = (0, 0, font["space"] * scale, (font["ascent"] + font["descent"] + shadowoffset) * scale)
      else:
        # width 1 and force blank
        draw.rectangle((0, 0, font["size"] * scale * maxwidthfactor, (font["ascent"] + font["descent"] + shadowoffset) * scale), fill=(0, 0, 0, 0), outline=None)
        imagebox = (0, 0, 1 * scale, (font["ascent"] + font["descent"]) * scale)
    else:
      # force width 1 for control characters and force blank
      if code in range(0, 31 + 1) or code in range(127, 159 + 1):
        draw.rectangle((0, 0, font["size"] * scale * maxwidthfactor, (font["ascent"] + font["descent"] + shadowoffset) * scale), fill=(0, 0, 0, 0), outline=None)
        imagebox = (0, 0, 1 * scale, (font["ascent"] + font["descent"] + shadowoffset) * scale)
    imagebox = (0, 0, imagebox[2], (font["ascent"] + font["descent"] + shadowoffset) * scale)
    if font["mono"]:
      # override with constant width for monospace fonts
      imagebox = (0, 0, font["space"] * scale, (font["ascent"] + font["descent"] + shadowoffset) * scale)
    crop = image.crop(imagebox)
    return crop, imagebox[2], imagebox[3] # return width-cropped glyph sprite, width and height

  for charset in charsets:
    print("", charset["name"], "charset")
    if check_update_needed([__file__, os.path.join(base_path, fonts[0]["path"]), os.path.join(base_path, fonts[1]["path"]), os.path.join(base_path, fonts[2]["path"])], os.path.join(base_path, charset["path"])):
      print("  ", "Generating", charset["path"])
      nml = open(os.path.join(base_path, charset["path"]+".tmp"), "w")
      for font in fonts:
        # skip non-baseset fonts for base charset
        if charset["name"] != "base" or font["base"]:
          currentcodesets = charset["codesets"]
          # for non-baseset fonts, prepend base charset
          if not font["base"]:
            currentcodesets = charsets[0]["codesets"] + currentcodesets
          # for monospace fonts, override maxwidthfactor
          maxwidthfactor = defaultmaxwidthfactor
          if font["mono"]:
            maxwidthfactor = 1
          # start output
          nml.write("// " + font["name"] + "\n")
          print(font["name"], "size", font["size"])
          for scale in scales:
            outpath = os.path.join(base_path, str(scale), "pygen", font["name"] + "_" + charset["name"] + "_32bpp.png")
            nml.write("// Scale " + str(scale) + "x\n")
            print("", "", str(scale) + "x scale\n")
            font["imfont"] = ImageFont.truetype(os.path.join(base_path, font["path"]), font["size"] * scale)
            printnml = False
            if scale == 1:
              # only print nml for 1x zoom
              printnml = True
            # generate sprites and record where they'll be placed in the sprite sheet, and write nml
            sprites = []
            index = -1
            for codeset in currentcodesets:
              if codeset["start"] == codeset["end"]:
                charrange = font["name"] + "_extra_codes_" + str(codeset["start"])
                blockname = "extra_" + font["name"] + "char_code_" + charrange
                templatename = "template_font_" + font ["name"] + "extra_code_" + charrange
                summary = "\"" + chr(codeset["start"]) + "\""
                characters = chr(codeset["start"])
              else:
                charrange =  str(codeset["start"]) + "to" + str(codeset["end"])
                blockname = "extra_" + font["name"] + "char_codes_" + charrange
                templatename = "template_font_" + font ["name"] + "extra_codes_" + charrange
                summary =  "\"" + chr(codeset["start"]) + "\" to \"" + chr(codeset["end"]) + "\""
                characters = "".join([chr(x) for x in range(codeset["start"], codeset["end"] - 1)])
              firstindex = index + 1
              if charset["name"] == "base":
                templatename = "template_spr" + str(firstindex + font["basesetoffs"])
                blockname = "spr" + str(firstindex + font["basesetoffs"])
              print("", "", "", codeset["end"] - codeset["start"] + 1, "characters:", summary)
              if printnml:
                nml.write("// Unicode " + str(codeset["start"]) + " to " + str(codeset["end"]) + "\n")
                #nml.write("// Characters \"" + characters + "\"\n")
                if "name" in codeset:
                  nml.write("// " + codeset["name"] + "\n")
                nml.write("template " + templatename + "(z) {\n")
              for code in range(codeset["start"], codeset["end"] + 1):
                index += 1
                sprite, w, h = get_glyph(font, scale, code)
                if scale != 1:
                  w += scale # Hack: Increases glyph width for 2x and 4x zooms, to account for any rounding error in glyph width when scaled up
                x = (index % outputcolumns) * (outputpadding + font["size"] * maxwidthfactor) + outputpadding
                y = floor(index / outputcolumns) * (outputpadding + font["ascent"] + font["descent"]) + outputpadding
                sprites.append({"sprite": sprite, "w": w, "h": h, "x": x, "y": y})
                if printnml:
                  if code in cropcodes:
                    # hack: custom character range X (window close) icon should be maximally cropped
                    nml.write("    [" + str(x) + "*z, "+str(y) + "*z, " + str(w) + "*z, " + str(h) + "*z, 0," + str(font["yoffs"]) + "*z] // " + str(code) + " \n")
                  else:
                    nml.write("    [" + str(x) + "*z, "+str(y) + "*z, " + str(w) + "*z, " + str(h) + "*z, 0," + str(font["yoffs"]) + "*z, NOCROP] // " + str(code) + "\n")
              if printnml:
                nml.write("}\n\n")
                if charset["name"] == "base":
                  nml.write("base_graphics " + blockname + "(" + str(firstindex + font["basesetoffs"]) + ", \"../graphics/fonts/" + str(scale) + "/pygen/" + font["name"] + "_" + charset["name"] + "_8bpp.png\") {\n")
                else:
                  nml.write("font_glyph " + blockname + "(" + font["code"] + ", " + hex(codeset["start"]) + ", \"../graphics/fonts/" + str(scale) + "/pygen/" + font["name"] + "_" + charset["name"] + "_8bpp.png\") {\n")
              else:
                nml.write("alternative_sprites(" + blockname + ", ZOOM_LEVEL_IN_" + str(scale) + "X, BIT_DEPTH_8BPP, \"../graphics/fonts/" + str(scale) + "/pygen/" + font["name"] + "_" + charset["name"] + "_8bpp.png\") {\n")
              nml.write("    " + templatename + "(" + str(scale) + ")\n")
              nml.write("}\n\n")
            # generate spritesheet
            rows = ceil(len(sprites) / outputcolumns)
            image = Image.new("RGBA", ((outputcolumns * (font["size"] * maxwidthfactor + outputpadding) + outputpadding) * scale, (rows * (font["ascent"] + font["descent"] + outputpadding) + outputpadding) * scale), (255, 255, 255, 255))
            draw = ImageDraw.Draw(image)
            for sprite in sprites:
              draw.rectangle((sprite["x"] * scale, sprite["y"] * scale, sprite["x"] * scale + sprite["w"] - 1, sprite["y"] * scale + sprite["h"] - 1), fill=(0, 0, 255, 255), outline=None)
              image.paste(sprite["sprite"], (sprite["x"] * scale, sprite["y"] * scale), sprite["sprite"])
            image.save(outpath)
      nml.close()
      # rename temp file to final file, to prevent partial output
      os.rename(os.path.join(base_path, charset["path"]+".tmp"), os.path.join(base_path, charset["path"]))
    else:
      print("  ", "Skipped", charset["path"])

if __name__ == "__main__":
  fonts_charactergrab(".")