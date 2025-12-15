# OpenGFX2 Changelog

## v0.8.1
Base sets:
* Fix internal baseset version (#223)

## v0.8
Base set:

* Sprites for new OpenTTD features
    * Bridge deck overlays
    * City and town icons for sprite font
    * Left-pointing arrow to sprite font
    * Vertical ellipsis used for badges menu (#196)
* Graphics improvements
    * Less repetitive toyland terrain style
    * Sharper gridlines (#169)
    * Revamped and 4x zoom underground-style logo
    * 4x zoom streamliner logo
    * Clearer NewGRF download list checkmark (#188)
    * Toyland river slope rocks
    * Improve water strobing and snow dither zoom out optimisations (#158)
* Translation
    * Numerous translations via eints
    * More gracefully handle unknown language IDs and add Maori
    * Consolidate string definitions to allow future NewGRF translation (#187)
    * Avoid string concatenation for baseset description for better translation (#174)
* Minor fixes
    * Set background of endgame graphics to 0x69 dark brown
    * Make cargo icons 10px tall to match normal font
    * Correct sprite font offset and clipping errors
    * Add missing baseset obg file url metadata
    * Add missing tall office block ground tiles (#185)
    * Add toyland rail tunnel icon (#182)
    * Fix track orientation for monorail level crossing (#183)
    * Fix cursors, caps lock and backspace on-screen keyboard icons (#166)
    * Tidy river tile shapes
    * Include 2x zoom tunnel icons in Classic baseset (#157)
    * Farm field fence/hedge offsets to remain within tile
    * Remove whole-tile flicker in toyland canal water animation
    * Improve internal graphics and coding docs
    * Incorrect image for 4x zoom 8bpp sprite for spr1545 (#168)

High Def base set:
* Graphics improvements
    * Fix 4x zoom water gridlines
    * Add various 4x zoom temperate town buildings

## v0.7
Base set:
* Redrawn 1x zoom train, monorail and maglev wagons.
* Redrawn 1x zoom lorries, including climate-specific variants.
* Redrawn 1x zoom busses.
* Redrawn 1x zoom monorail and maglev engines.
* Style-unified 1x zoom rail engines.
* Refined 1x zoom boat graphics.
* Improved 1x zoom company colour visibility on hovercraft.
* Refined rock contrast and brightness, 1x and 4x zoom.
* Support for (snowy) rock overlays, 1x and 4x zoom.
* Improved contrast and tiling of 1x zoom rail.
* Fixed missing pixels from 1x and 4z zoom autorail selectors.
* Detail and company colour for 1x zoom docks.
* Improved 1x zoom maglev station roof.
* 2x zoom 8bpp manager faces.
* Select refined manager face features.
* Improved 8bpp conversion of manager faces.
* Fix manager face feature alignments.
* Fix broken manager face recolouring.
* Fix missing manager face woman's hairstyle.
* Brighter 1x zoom oil wells to stand out from terrain.
* Refined 1x zoom toyland industry sprites.
* Add shinyness to 1x zoom toyland trees.
* Add 1x and 2x zoom toyland cola cargo icon.
* Add 2x zoom sleepy cursor.
* Add 1x and 4x zoom gridlineless level crossing variants.
* Add 1x and 4x zoom climate grass switch-sensitive level crossings.
* Make road markings consistent when switching climates.
* Improved 1x and 4x zoom rail tunnel portals.
* Fix 4x zoom one-way roads.
* Fix stray white bar on 4x zoom plantations.
* Refactor graphics generation pipeline to use `make`.
* Check whether graphics requiring update from script changes.
* Fix missing 210 5-entry pallete series.

NewGRFs:
* OpenGFX2+ Trams, 4 generations of generic trams at 1x zoom.
* Fix rock recolouring and add yellow rocks in object NewGRF.

## v0.6
Base set:
* 1x and 4x road waypoint graphics.
* Better 4x rail and monorail alignment on tiles.
* 4x zoom tunnels.
* 4x zoom bridges.
* 4x zoom block, path and pre-signals.
* Prototype/first 4x zoom road and rail station graphics.
* 4x zoom logo.
* Improved 4x temperate tree detail.
* Traditional and simplified Chinese translations.
* Various bugfixes, including:
* Fixed 1526 house miscoded as a ground sprite.
* Fixed miscoded multiplayer icons.
* Fixed large sprite font alignment.
* Minor sprite and GUI element alignment tweaks.
* Fixed one way road alignment errors.
* Fixed farm fence alignment.
* Fixed incorrect SW dead end tram track sprite.
* Fixed incorrect transparent blue for copper ore wagon.

NewGRFs:
* Fixed lighthouse and transmitter alignment in object NewGRF.

## v0.5
Base set:
* All GUI icons at 1x and 2x zoom, with some at 4x.
* Improved cursors, all at 1x and 2x zoom.
* Additional cursor styles.
* Build sprite font from TTFs, for full sprite font at 2x and 4x zoom.
* TTD-style custom monospaced sprite font, from TTF.
* Extended sprite font range to also cover Cyrillic and Greek alphabets.
* Prototype/first 4x rail vehicle sprites.
* Various additional bug fixes, including:
* Fix bridge colour, recolour and leg glitches.
* Fix/tweak town tree graphics.
* Fix Various rock and slope shading glitches.

NewGRFs:
* New standalone objects NewGRF, with fields, forests, rocks and building objects.
* Fix tree NewGRF to also replace cacti and palm trees.

## v0.4
Base set:
* 4x zoom trees for normal climates, including improved growth/death stages.
* 4x zoom tree/plantation industries.
* 4x zoom improved pixel art detailing of terrain.
* Improved maglev level crossings.
* Various bug fixes.

NewGRFs:
* New standalone trees NewGRF.

Known issues:
* If you're using a nightly, make sure you're using one from later than 29/10/2023, otherwise all climates will end up looking like temperate!

## v0.3
Base set:
* Baseset parameters, for baseset parameter support when OpenTTD 14.0 arrives.
* Removed pixel jitter in animated industries, and similar tweaks.
* Expanded 2x scale GUI scaling support.
* Prototype pixel art 4x zoom trees for Arctic.
* Various bug fixes.

Settings NewGRF:
* Preparation for depreciation when OpenTTD 14.0 arrives.

NewGRFs:
* New rail stations and waypoints NewGRF, just waypoints for now.
* Fixes for standalone behaviour of the landscape NewGRF.

Known issues:
* If you're using a nightly, make sure you're using one from later than 29/10/2023, otherwise all climates will end up looking like temperate!

## v0.21
Minor bugfix release.

Base set:
* Switch to integer version numbering for internal use, decimal not supported by OpenTTD for version comparisons.
* Minor bug fixes.

## v0.2
Base set:
* Bug fixes from v0.1, including a few game-breaking missing (white box) sprites.
* Initial support for 2x GUI scaling (including in 'Classic' variant).

Settings NewGRF:
* Parameter control of grass (terrain tile), foundation and tree style per climate. Almost fully mix-and-match.

NewGRFs:
* New standalone landscape NewGRF.

Backend:
* Multithreading for much faster 32bpp to 8bpp sprite conversion.

## v0.1
Base set:
* First OpenGFX-independent baseset.
* 8bpp 1x zoom 'Classic' variant.
* 32bpp 4x zoom 'High Def' variant.
'Classic' is a complete baseset. 'High Def' 32bpp and 4x zoom sprites are not universally complete, and uses 8bpp 1x zoom fallbacks.

Settings NewGRF:
* Sets parameters which the extra grf in the baseset reads.
* Configure presence/absence of gridlines, logo style, cursor styles.
