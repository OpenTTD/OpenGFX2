# Versions
# nice user-facing version naming
NAMING_VERSION := 0.7

# Default target
.PHONY: all
all: baseset baseset_highdef newgrf

# Basesets
# "Classic" 8bpp 1x zoom baseset
.PHONY: baseset
baseset: baseset/OpenGFX2_Classic-$(NAMING_VERSION).zip

baseset/OpenGFX2_Classic-$(NAMING_VERSION).zip: baseset/OpenGFX2_Classic-$(NAMING_VERSION).tar
	cd baseset && zip -9 -r OpenGFX2_Classic-$(NAMING_VERSION).zip OpenGFX2_Classic-$(NAMING_VERSION).tar

# "High Def" 32bpp 4x zoom baseset
.PHONY: baseset_highdef
baseset_highdef: baseset/OpenGFX2_HighDef-$(NAMING_VERSION).zip

baseset/OpenGFX2_HighDef-$(NAMING_VERSION).zip: baseset/OpenGFX2_HighDef-$(NAMING_VERSION).tar
	cd baseset && zip -9 -r OpenGFX2_HighDef-$(NAMING_VERSION).zip OpenGFX2_HighDef-$(NAMING_VERSION).tar

# Base set packaging
.PRECIOUS: OpenGFX2_Classic-$(NAMING_VERSION).tar OpenGFX2_HighDef-$(NAMING_VERSION).tar
BASESET_GRFS = ogfx2c_arctic ogfx2e_extra ogfx2h_tropical ogfx2i_logos ogfx2t_toyland ogfx21_base
BASESET_DOCS = README.md LICENSE CHANGELOG.md

baseset/OpenGFX2_Classic-$(NAMING_VERSION).tar: baseset/opengfx2_8.obg $(BASESET_DOCS) $(foreach grf,$(BASESET_GRFS),baseset/$(grf)_8.grf)
	mkdir -p baseset/OpenGFX2_Classic-$(NAMING_VERSION)
	cp README.md baseset/OpenGFX2_Classic-$(NAMING_VERSION)/readme.md
	cp LICENSE baseset/OpenGFX2_Classic-$(NAMING_VERSION)/license.txt
	cp CHANGELOG.md baseset/OpenGFX2_Classic-$(NAMING_VERSION)/changelog.md
	cp $(foreach grf,$(BASESET_GRFS),baseset/$(grf)_8.grf) baseset/OpenGFX2_Classic-$(NAMING_VERSION)/
	cp baseset/opengfx2_8.obg baseset/OpenGFX2_Classic-$(NAMING_VERSION)/
	cd baseset && tar -cf OpenGFX2_Classic-$(NAMING_VERSION).tar OpenGFX2_Classic-$(NAMING_VERSION)/
	rm -r baseset/OpenGFX2_Classic-$(NAMING_VERSION)

baseset/OpenGFX2_HighDef-$(NAMING_VERSION).tar: baseset/opengfx2_32ez.obg $(BASESET_DOCS) $(foreach grf,$(BASESET_GRFS),baseset/$(grf)_32ez.grf)
	mkdir -p baseset/OpenGFX2_HighDef-$(NAMING_VERSION)
	cp README.md baseset/OpenGFX2_HighDef-$(NAMING_VERSION)/readme.md
	cp LICENSE baseset/OpenGFX2_HighDef-$(NAMING_VERSION)/license.txt
	cp CHANGELOG.md baseset/OpenGFX2_HighDef-$(NAMING_VERSION)/changelog.md
	cp $(foreach grf,$(BASESET_GRFS),baseset/$(grf)_32ez.grf) baseset/OpenGFX2_HighDef-$(NAMING_VERSION)/
	cp baseset/opengfx2_32ez.obg baseset/OpenGFX2_HighDef-$(NAMING_VERSION)/
	cd baseset && tar -cf OpenGFX2_HighDef-$(NAMING_VERSION).tar OpenGFX2_HighDef-$(NAMING_VERSION)/
	rm -r baseset/OpenGFX2_HighDef-$(NAMING_VERSION)

# OBG for baseset
# FORCE, as baseset_generate_obg checks for necessary updates
.PRECIOUS: baseset/opengfx2_8.obg baseset/opengfx2_32ez.obg

baseset/opengfx2_8.obg: baseset/baseset_generate_obg.py baseset/lang/*.lng $(foreach grf,$(BASESET_GRFS),baseset/$(grf)_8.grf) $(foreach grf,$(BASESET_GRFS),baseset/$(grf)_8.md5)
	python3 baseset/baseset_generate_obg.py 8 baseset/

baseset/opengfx2_32ez.obg: baseset/baseset_generate_obg.py baseset/lang/*.lng $(foreach grf,$(BASESET_GRFS),baseset/$(grf)_32ez.grf) $(foreach grf,$(BASESET_GRFS),baseset/$(grf)_32ez.md5)
	python3 baseset/baseset_generate_obg.py 32ez baseset/

# GRF and MD5, via NML intermediate, for baseset
# FORCE, as nml_preprocessor includes arbitrary pnml files
.PRECIOUS: baseset/%.grf baseset/%.md5 baseset/%.nml

baseset/%_8.grf: graphics_1 baseset/lang/*.lng FORCE
	$(eval PREF=$(word 1, $(subst _, ,$(basename $(notdir $@)))))
	$(eval NAME=$(word 2, $(subst _, ,$(basename $(notdir $@)))))
	$(eval ZOOM=$(word 3, $(subst _, ,$(basename $(notdir $@)))))
	python3 templates/nml_preprocessor.py baseset/$(PREF)_$(NAME).pnml $(ZOOM)
	cd baseset && nmlc -p DOS --quiet -c $(PREF)_$(NAME)_$(ZOOM).nml --md5 $(PREF)_$(NAME)_$(ZOOM).md5

baseset/%_32ez.grf: graphics_4 baseset/lang/*.lng FORCE
	$(eval PREF=$(word 1, $(subst _, ,$(basename $(notdir $@)))))
	$(eval NAME=$(word 2, $(subst _, ,$(basename $(notdir $@)))))
	$(eval ZOOM=$(word 3, $(subst _, ,$(basename $(notdir $@)))))
	echo $(PREF) $(NAME) $(ZOOM)
	python3 templates/nml_preprocessor.py baseset/$(PREF)_$(NAME).pnml $(ZOOM)
	cd baseset && nmlc -p DOS --quiet -c $(PREF)_$(NAME)_$(ZOOM).nml --md5 $(PREF)_$(NAME)_$(ZOOM).md5

# NewGRFs
.PHONY: newgrf
NEWGRFS = landscape objects settings stations trees trams
newgrf: $(foreach grf,$(NEWGRFS),newgrf/ogfx2_$(grf).grf)

# GRF, via NML intermediate, for NewGRFs
# FORCE, as nml_preprocessor includes arbitrary pnml files
.PRECIOUS: newgrf/ogfx2_%.grf newgrf/ogfx2_%.nml

newgrf/%.grf: graphics_4 FORCE
	$(eval PREF=$(word 1, $(subst _, ,$(basename $(notdir $@)))))
	$(eval NAME=$(word 2, $(subst _, ,$(basename $(notdir $@)))))
	echo $(PREF) $(NAME)
	python3 templates/nml_preprocessor.py newgrf/$(PREF)_$(NAME).pnml 32ez
	mv newgrf/$(PREF)_$(NAME)_32ez.nml newgrf/$(PREF)_$(NAME).nml
	cd newgrf && nmlc -p DOS --quiet -c -l lang/$(NAME) $(PREF)_$(NAME).nml

# Graphics
# Python generation of all graphics from PNG sources

# FORCE as generate_graphics.py will check what updates are necessary
.PHONY: graphics
graphics: graphics_4.tmp

.PHONY: graphics_4
graphics_4: graphics_4.tmp

.PHONY: graphics_1
graphics_1: graphics_1.tmp

.PRECIOUS: graphics_%.tmp
graphics_%.tmp: graphics/fonts/openttd-ttf FORCE
	cd graphics/fonts/openttd-ttf && git pull
	$(eval ZOOM=$(word 2, $(subst _, ,$(basename $(notdir $@)))))
	python3 graphics/generate_graphics.py $(ZOOM)

# Get font git dependencies
graphics/fonts/openttd-ttf:
	cd graphics/fonts && git clone https://github.com/OpenTTD/OpenTTD-TTF openttd-ttf

# Clean
.PHONY: clean
clean: clean_baseset clean_newgrf clean_graphics

# Clean baseset
.PHONY: clean_baseset
clean_baseset:
	rm -f baseset/*.grf baseset/*.md5 baseset/*.obg baseset/*.tar baseset/*.nml
	rm -rf baseset/.nmlcache

# Clean NewGRFs
.PHONY: clean_newgrf
clean_newgrf:
	rm -f newgrf/*.grf newgrf/*.nml
	rm -rf newgrf/.nmlcache

# Clean graphics
.PHONY: clean_graphics
clean_graphics:
	rm -f graphics*.tmp
	find graphics -type d -name "pygen" -exec rm -rf {} +
	find graphics -type f -name "*_8bpp.png" -exec rm {} +
	find graphics -type f -name "*_bt32bpp.png" -exec rm {} +
	find graphics -type f -name "*_rm32bpp.png" -exec rm {} +
	find graphics -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf graphics/fonts/openttd-ttf

FORCE: ;
