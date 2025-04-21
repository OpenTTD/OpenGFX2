# How to release a new version of OpenGFX2

1. Update the changelog:
   * `CHANGELOG.md` with key fixes and features

2. Bump the versions:
   * User facing version in `makefile`
   * Base set version in `baseset/baseset_generate_obg.py`
   * Base set version string in `baseset/lang/english.lng`
   * Base set `extra.grf` version in `baseset/nml/extra-header.pnml`
   * NewGRF versions in `newgrf/nml/<newgrf_name>/<newgrf_name>-header.pmnl`
   * `extra.grf`/`opengfx2_settings.grf` co-compatibility check in `baseset/nml/extra-header.pnml`

For better or worse, base set currently uses fractional (0.1, 0.2, ...) versioning and NewGRFs use integer (1, 2, ...) versioning.
