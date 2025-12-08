# How to release a new version of OpenGFX2

1. Update the changelog and bump the version:
   * `CHANGELOG.md` with key fixes and features
   * User-facing version `USER_VERSION` in `makefile`

Make a PR and, once merged:

2. Do a clean build of master:
   * `make clean && make all`

3. On Github, go to "Releases", "Draft a new release":
   * Draft the release text (a refined copy of the changelog) and title
   * Attach baseset (both Classic and High Def) `tar`s from `baseset/` and NewGRF `grf`s from `newgrf`.
   * Create a new tag with the user-facing version
Creation of the new version tag on publishing the release will trigger a new release to the [OpenTTD CDN](https://cdn.openttd.org/opengfx2_classic-releases/) under the user-facing version.
