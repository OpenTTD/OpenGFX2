# How to release a new version of OpenGFX2

1. Update the changelog:
   * `CHANGELOG.md` with key fixes and features

2. Bump the versions:
   * Base set version in `baseset/baseset_generate_obg.py` (`descriptionversion`)
   * Base set `extra.grf` version in `baseset/nml/extra-header.pnml` (`grf` block, `version`)
   * NewGRF versions in `newgrf/nml/<newgrf_name>/<newgrf_name>-header.pmnl` (`grf` block, `version`)
   * `extra.grf`/`opengfx2_settings.grf` co-compatibility check in `baseset/nml/extra-header.pnml` (in `if (grf_future_status("OGZ\1")==1)` block)

The main user facing version in `makefile` (`NAMING_VERSION`) is automatically taken from the repository version.

For better or worse, base set currently uses fractional (0.1, 0.2, ...) versioning and NewGRFs use integer (1, 2, ...) versioning.

3. On Github, go to "Releases", "Draft a new release":
   * Draft the release text (a refined copy of the changelog) and title.
   * Attach baseset (both Classic and High Def) `tar`s and NewGRF `grf`s
   * Create a new tag with the appropriate version.
Creation of the new version tag on publishing the release will trigger a new release to the OpenTTD CDN.
