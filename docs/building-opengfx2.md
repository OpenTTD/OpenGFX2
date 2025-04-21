# Building OpenGFX2
These notes are for if you want to build OpenGFX2 from the source files. If you just want to download OpenGFX2 then you don't need to worry about these.

Requires `git lfs` for large file handling. Once `git lfs` is installed then clone using `git` as normal.

Requires a system with `make`, `nmlc`, `git` and  `python3` with `PIL`, `blend-modes`, `numpy`, `skimage`, `tqdm`. This has been developed using Windows Subsystem for Linux (WSL) and might have peculiarities (eg. incorrect file permissions) on a real Linux install.

### To build
Clone the repository, navigate to the repository root directory and run `make all`. It will take a long time...

The built baseset will be in `baseset/`, making different versions called `OpenGFX2_<variant>-<version>.tar` and `.zip`.
You can (re)build only the "Classic" 8bpp 1x zoom baseset using `make baseset` or the "High Def" 32bpp 4x zoom baseset using `make baseset_highdef`.

The built NewGRF(s) will be in `newgrf/`, making various `.grf` files.
You can (re)build only the NewGRFs using `make newgrf`.

You can (re)build only the graphics using `make graphics`.

Intermediate files can be removed for a clean build using `make clean`, or `make clean_graphics`, `make clean_baseset` or `make clean_newgrf` for graphics, baseset and newgrf files respectively.

### Build process notes
Image processing makes a bunch of intermediate files, particularly `*_8bpp.png` and things in `pygen` directories. Others are `_bt32bpp.png`, `_rm32bpp.png`. These files are assumed to be temporary intermediates, and any user-modified versions will be blindly overwritten. Make sure you look at `.gitignore` see which files this applies to.

Files processed by `python` and encoded by `nml` are `.png` files, but those may be derived from other sources. Raw sprites were variously drawn\generated in Paint.NET, Aseprite, Blender and more. Conversion from those raw sources to `.png` files is not part of the build process - it must be done manually.

All sprite sheets are generated from source `png` files by `graphics/generate_graphics.py`. However, [OpenTTD-TTF](https://github.com/OpenTTD/OpenTTD-TTF) must have first been cloned to `graphics/fonts/openttd-ttf`. `make all` or `make graphics` handles this for you though.
