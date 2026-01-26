#!/usr/bin/env python3

"""
Loads a pnml file and:
Populates with information from #import lines.
Removes comments to configure extra zoom and 32bpp alternative sprites.

Import lines in the pnml must be formatted:
#import "path/to/nml/file.nml"
Path must be relative, quoted, and no additional whitespace is tolerated.

Extra zoom and 32bpp alternative sprites are controlled by removing comment strings exactly matching:
"#ez " for extra zoom sprites
"#32 " for 32bpp sprites
(use "#32 #ez " for 32bpp extra zoom sprites)

Positional arguments:
1. base name (base pnml name with extension)
2. string including ez and/or 32 (if matched, include sprites of these types)
3. optional string "exclude_name_suffix" (if matched, do not append _8, _8ez, _32 or _32ez to the output file name)

Output:
nml file with the same name as the pnml file appended with type (_8, _8ez, _32 or _32ez)

Only updates the output file if the input file, imported files, or the script has been modified since the last time the output was generated.
"""

import sys, os

def preprocess_pnml(pnml_path, newgrf_version, high_bitdepth = False, extra_zoom = False, exclude_name_suffix = False):
  def get_name():
    """
    Set the name of the nml variant based on the options.
    """
    name = "8"
    if high_bitdepth:
      name = "32"
    if extra_zoom:
      name += "ez"
    return name

  def check_nml_exists():
    """
    Check if the nml file already exists.
    """
    return os.path.exists(nml_path)

  def check_script_change():
    """
    Check if the script has been modified since the last time the nml was generated.
    """
    return os.path.getmtime(__file__) > os.path.getmtime(nml_path)
  
  def check_pnml_change():
    """
    Check if the pnml has been modified since the last time the nml was generated.
    """
    return os.path.getmtime(pnml_path) > os.path.getmtime(nml_path)

  def check_imports_change():
    """
    Check if the imports have been modified since the last time the nml was generated.
    """
    imports = list_imports()
    for import_path in imports:
      if os.path.getmtime(import_path) > os.path.getmtime(nml_path):
        return True
    return False

  def handle_version_line(line):
    """
    Check if the line is a version line, and return the NML-formatted version if it is.
    """
    # comment defining version
    comment_version = "# version_line_marker #"

    if line.strip() == comment_version:
      prefix = line.split(comment_version)[0]
      return prefix + "version: " + newgrf_version + ";"
    return line

  def check_import_line(line):
    """
    Check if the line is an import line, and return the path if it is.
    """
    # comment defining import
    comment_import = "#include"

    if line.startswith(comment_import):
      return line[len(comment_import)+2:-1]
    return None

  def list_imports():
    """
    List all imports in the pnml file.
    """
    imports = []
    with open(pnml_path, "r") as pnml:
      lines = pnml.read().splitlines()
      for line in lines:
        if check_import_line(line) is not None:
          imports.append(os.path.join(base_path, check_import_line(line)))
    return imports

  def handle_alternates(line):
    """
    Handle inclusion of alternate high bit depth and extra zoom sprites.
    """
    # define alternate comment strings
    comment_alternate = ["#ez ", "#32 "]

    settings_alternate = [extra_zoom, high_bitdepth]
    for c in range(len(comment_alternate)):
      comment = comment_alternate[c]
      if comment in line:
        if settings_alternate[c]:
          line = line.replace(comment, "")
        else:
          line = line.replace(comment, comment.replace("#", "//"))
    return line

  print("Preprocessing", pnml_path)
  if not exclude_name_suffix:
    nml_path = pnml_path[:-len(".pnml")] + "_" + get_name() + ".nml"
  else:
    nml_path = pnml_path[:-len(".pnml")] + ".nml"
  print("Outputting", nml_path)
  base_path = os.path.dirname(pnml_path)
  if check_nml_exists() and not check_script_change() and not check_pnml_change() and not check_imports_change():
    # output already exists and is up to date
    print("Output is up to date.")
    return
  if base_path == "":
    print("Working in current directory")
  else:
    print("Working in", base_path)

  with open(nml_path, "w") as nml:
    try:
      with open(sys.argv[1], "r") as pnml:
        lines = pnml.read().splitlines()
        for line in lines:
          if check_import_line(line) is not None:
            import_path = check_import_line(line)
            print("Including", import_path)
            try:
              with open(os.path.join(base_path, import_path), "r") as include:
                include_lines = include.read().splitlines()
                for include_line in include_lines:
                  include_line = handle_version_line(include_line)
                  include_line = handle_alternates(include_line)
                  nml.write(include_line + "\n")
            except FileNotFoundError:
              print("File not found:", os.path(base_path, import_path))
          else:
            include_line = handle_version_line(line)
            include_line = handle_alternates(include_line)
            nml.write(include_line + "\n")
    except FileNotFoundError:
      print("File not found:", sys.argv[1] + ".pnml")

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print("Usage: baseset_generate_obg.py <pnml_path> <newgrf_version> [type_string] [exclude_name_suffix]")
    sys.exit(1)
  pnml_path = sys.argv[1]
  newgrf_version = sys.argv[2]
  high_bitdepth = False
  extra_zoom = False
  if len(sys.argv) > 3:
    if "32" in sys.argv[3]:
      high_bitdepth = True
    if "ez" in sys.argv[3]:
      extra_zoom = True
  exclude_name_suffix = False
  if len(sys.argv) > 4:
    if sys.argv[4] == "exclude_name_suffix":
      exclude_name_suffix = True
  preprocess_pnml(pnml_path, newgrf_version, high_bitdepth, extra_zoom, exclude_name_suffix)
