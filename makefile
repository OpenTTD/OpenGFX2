# Version reported to users
USER_VERSION := 0.8

# Always run version detection, so we always have an accurate modified flag
REPO_VERSIONS := $(shell AWK="$(AWK)" "./findversion.sh")
REPO_MODIFIED := $(shell echo "$(REPO_VERSIONS)" | cut -f 3 -d'	')
# Use autodetected revisions
REPO_VERSION := $(shell echo "$(REPO_VERSIONS)" | cut -f 1 -d'	')
REPO_DATE := $(shell echo "$(REPO_VERSIONS)" | cut -f 2 -d'	')
REPO_HASH := $(shell echo "$(REPO_VERSIONS)" | cut -f 4 -d'	')

# File naming version
NAMING_VERSION := $(REPO_VERSION)
NAMING_CDN := opengfx2_classic
# Version reported to OpenTTD, days since 2000
BASESET_VERSION := $(shell python3 -c "from datetime import date; d='$(REPO_DATE)'; print((date(int(d[:4]),int(d[4:6]),int(d[6:8]))-date(2000,1,1)).days)")

# Version information target, write if changed so that dependent targets can be updated based on changes
makefile.vcs: FORCE
	echo "REPO_HASH = $(REPO_HASH)" > $@.new
	echo "REPO_DATE = $(REPO_DATE)" >> $@.new
	echo "REPO_VERSION = $(REPO_VERSION)" >> $@.new
	echo "BASESET_VERSION = $(BASESET_VERSION)" >> $@.new
	echo "USER_VERSION = $(USER_VERSION)" >> $@.new
	echo "NAMING_VERSION = $(NAMING_VERSION)" >> $@.new
	echo "NAMING_CDN = $(NAMING_CDN)" >> $@.new
	cmp -s $@.new $@ || mv $@.new $@
	rm -f $@.new

.PHONY: clean_version
clean_version:
	rm -f makefile.vcs

# Default target
.PHONY: all
all: baseset baseset_highdef newgrf

# Basesets
# "Classic" 8bpp 1x zoom baseset
.PHONY: baseset
baseset: baseset/OpenGFX2_Classic-$(NAMING_VERSION).zip makefile.vcs

baseset/OpenGFX2_Classic-$(NAMING_VERSION).zip: baseset/OpenGFX2_Classic-$(NAMING_VERSION).tar makefile.vcs
	cd baseset && zip -9 -r OpenGFX2_Classic-$(NAMING_VERSION).zip OpenGFX2_Classic-$(NAMING_VERSION).tar

# "High Def" 32bpp 4x zoom baseset
.PHONY: baseset_highdef
baseset_highdef: baseset/OpenGFX2_HighDef-$(NAMING_VERSION).zip makefile.vcs

baseset/OpenGFX2_HighDef-$(NAMING_VERSION).zip: baseset/OpenGFX2_HighDef-$(NAMING_VERSION).tar makefile.vcs
	cd baseset && zip -9 -r OpenGFX2_HighDef-$(NAMING_VERSION).zip OpenGFX2_HighDef-$(NAMING_VERSION).tar

# Base set packaging
.PRECIOUS: OpenGFX2_Classic-$(NAMING_VERSION).tar OpenGFX2_HighDef-$(NAMING_VERSION).tar makefile.vcs
BASESET_GRFS = ogfx2c_arctic ogfx2e_extra ogfx2h_tropical ogfx2i_logos ogfx2t_toyland ogfx21_base
BASESET_DOCS = README.md LICENSE CHANGELOG.md

baseset/OpenGFX2_Classic-$(NAMING_VERSION).tar: baseset/opengfx2_8.obg $(BASESET_DOCS) $(foreach grf,$(BASESET_GRFS),baseset/$(grf)_8.grf) makefile.vcs
	mkdir -p baseset/OpenGFX2_Classic-$(NAMING_VERSION)
	cp README.md baseset/OpenGFX2_Classic-$(NAMING_VERSION)/readme.md
	cp LICENSE baseset/OpenGFX2_Classic-$(NAMING_VERSION)/license.txt
	cp CHANGELOG.md baseset/OpenGFX2_Classic-$(NAMING_VERSION)/changelog.md
	cp $(foreach grf,$(BASESET_GRFS),baseset/$(grf)_8.grf) baseset/OpenGFX2_Classic-$(NAMING_VERSION)/
	cp baseset/opengfx2_8.obg baseset/OpenGFX2_Classic-$(NAMING_VERSION)/
	cd baseset && tar -cf OpenGFX2_Classic-$(NAMING_VERSION).tar OpenGFX2_Classic-$(NAMING_VERSION)/
	rm -r baseset/OpenGFX2_Classic-$(NAMING_VERSION)

baseset/OpenGFX2_HighDef-$(NAMING_VERSION).tar: baseset/opengfx2_32ez.obg $(BASESET_DOCS) $(foreach grf,$(BASESET_GRFS),baseset/$(grf)_32ez.grf) makefile.vcs
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

baseset/opengfx2_8.obg: baseset/baseset_generate_obg.py baseset/lang/*.lng $(foreach grf,$(BASESET_GRFS),baseset/$(grf)_8.grf) $(foreach grf,$(BASESET_GRFS),baseset/$(grf)_8.md5) makefile.vcs
	python3 baseset/baseset_generate_obg.py $(BASESET_VERSION) $(USER_VERSION) 8 baseset/

baseset/opengfx2_32ez.obg: baseset/baseset_generate_obg.py baseset/lang/*.lng $(foreach grf,$(BASESET_GRFS),baseset/$(grf)_32ez.grf) $(foreach grf,$(BASESET_GRFS),baseset/$(grf)_32ez.md5) makefile.vcs
	python3 baseset/baseset_generate_obg.py $(BASESET_VERSION) $(USER_VERSION) 32ez baseset/

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
	cd newgrf && nmlc -p DOS --quiet -c -l ../baseset/lang $(PREF)_$(NAME).nml

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
clean: clean_baseset clean_newgrf clean_graphics clean_version

# Clean baseset
.PHONY: clean_baseset clean_version
clean_baseset:
	rm -f baseset/*.grf baseset/*.md5 baseset/*.obg baseset/*.tar baseset/*.nml
	rm -rf baseset/.nmlcache

# Clean NewGRFs
.PHONY: clean_newgrf clean_version
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

# Glue to work like OpenGFX Makefile
.PHONY: maintainer-clean
maintainer-clean: clean

# Glue to work like OpenGFX Makefile
.PHONY: bundle_zip
bundle_zip: baseset/OpenGFX2_Classic-$(NAMING_VERSION).zip makefile.vcs
	cp baseset/OpenGFX2_Classic-$(NAMING_VERSION).zip $(NAMING_CDN)-$(NAMING_VERSION)-all.zip

# Glue to work like OpenGFX Makefile
.PHONY: bundle_xsrc
bundle_xsrc:
	mkdir -p $(NAMING_CDN)-$(NAMING_VERSION)-source
	git archive --format=tar HEAD | tar xf - -C $(NAMING_CDN)-$(NAMING_VERSION)-source/
	rm -rf $(NAMING_CDN)-$(NAMING_VERSION)-source/.git $(NAMING_CDN)-$(NAMING_VERSION)-source/.gitattributes $(NAMING_CDN)-$(NAMING_VERSION)-source/.gitignore $(NAMING_CDN)-$(NAMING_VERSION)-source/.github
	./findversion.sh > $(NAMING_CDN)-$(NAMING_VERSION)-source/.ottdrev
	tar -cf $(NAMING_CDN)-$(NAMING_VERSION)-source.tar $(NAMING_CDN)-$(NAMING_VERSION)-source
	xz -ef $(NAMING_CDN)-$(NAMING_VERSION)-source.tar

FORCE: ;
