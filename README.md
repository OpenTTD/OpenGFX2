# OpenGFX2
# ![opengfx2_titletext](https://github.com/OpenTTD/OpenGFX2/assets/2762690/1adabdf4-baf8-48b2-ae35-279c3d808d0e)

"OpenGFX2" graphics base set for [OpenTTD](https://github.com/OpenTTD/OpenTTD). It is drawn in a classic 8-bit pixel art style and tries to capture the feel of the original Transport Tycoon graphics by using similar colour schemes, building and object designs, etc. There are two variants:
* `OpenGFX2 Classic`: An original graphics-style base set, 8-bit at 1x zoom (64 px wide tiles).
* `OpenGFX2 High Def`: An enhanced base set, using 32-bit images for smoother shading at 4x zoom (256 px wide tiles) for more detail when zooming in.

OpenGFX2 is a spiritual successor to [OpenGFX](https://github.com/OpenTTD/OpenGFX). Think of it as "OpenGFX version 2", or maybe that should be "OpenGFX director's edition", "refactored OpenGFX", or perhaps "OpenGFX extra zoom" or "OpenGFX 32-bit". Or some combination of all of them. OpenGFX2 is derived from OpenGFX, but extensively redrawn or revised from original 32-bit sources. Almost all sprites have been updated or revised. It features far better organisation of sprites, extensive use of automated composite sprite generation (using Python of dubious quality) and is drawn and coded with extra zoom levels and 32-bit in mind.

OpenGFX2 is a totally separate graphics set to zBase.

## Current Status

`OpenGFX2 Classic` is complete and ready to use. There might be bugs though, please post any you find [on GitHub](https://github.com/OpenTTD/OpenGFX2/issues).

`OpenGFX2 High Def` isn't complete, but can be used. The landscape (grass, water, trees) and infrastructure (road, rail, bridges) are mostly complete, but the vehicles and houses are generally not. Please post any bugs [to GitHub](https://github.com/OpenTTD/OpenGFX2/issues), except for missing 4x zoom sprites - we know which are missing!

## Quick start

### In-game content downloader / BaNaNaS
It is easiest to use the in-game content downloader (`Check Online Content` in the OpenTTD main menu).

To install, search for `OpenGFX2`, tick the checkbox next to "OpenGFX2 Classic" Base graphics, and hit `Download`.

To set as the base graphics set, go to `Game Options > (Graphics) > Base Graphics` from the OpenTTD main menu. Select `OpenGFX2 Classic`, then close the `Game Options` window.

### Manual download
Download a release from [the prebuilt GRF releases](https://github.com/OpenTTD/OpenGFX2/tags) and install using the instructions below.

These are early release previews not available in the in-game content downloader. This includes base set versions (the "High Def" 32-bit 4x zoom version) and NewGRFs not yet available through the in-game downloader.

### Installation
Install the baseset by copying `opengfx2_8.tar` and/or `opengfx2_32ez.tar` into the `baseset` directory for your OpenTTD installation.

Install the newgrfs by copying each `.grf` file into the `NewGRF` directory for your OpenTTD installation.

To set as the base graphics set, go to `Game Options>(Graphics)>Base Graphics` Set and select `OpenGFX2 Classic` (8-bit 1x zoom version) or `OpenGFX2 High Def` (32-bit 4x zoom version).

OpenGFX2 has graphical user preferences. These can be configured in `Game Options>(Graphics)>Base graphics set>Set parameters`. These settings are local graphical changes only. You can freely change them and use them with any save-game, use any server, etc.

If you instead want for force a game or server to use OpenGFX2 graphics you can use the OpenGFX2 NewGRFs.

Prior to OpenTTD 14.0 (specifically nightlies prior to 30/10/2023 or before Github commit e81313e) OpenTTD did not have a way to configure base set parameters. The `OpenGFX2 Settings` NewGRF provides a workaround: Go to `NewGRF Settings`, find `OpenGFX2 Settings` and add to `Active NewGRF files`. Then, select `OpenGFX2 Settings` in the `Active NewGRF files list` and select `Set parameters` then adjust the settings.

Install other NewGRFs as normal using `NewGRF settings`.

## Building
If you wish to build your own version of OpenGFX2 instead of using our prebuilt version, you can follow [these instructions](docs/building-opengfx2.md).
