# Default target
.PHONY: all
all: baseset baseset_highdef newgrf

# Basesets
# "Classic" 8bpp 1x zoom baseset
.PHONY: baseset
baseset: baseset/opengfx2_8.tar

# "High Def" 32bpp 4x zoom baseset
.PHONY: baseset_highdef
baseset_highdef: baseset/opengfx2_32ez.tar

# All baseset variants
.PHONY: baseset_32 baseset_8ez
baseset_8: baseset/opengfx2_8.tar
baseset_32: baseset/opengfx2_32.tar
baseset_8ez: baseset/opengfx2_8ez.tar
baseset_32ez: baseset/opengfx2_32ez.tar

# Generalised baseset
.PRECIOUS: opengfx2_%.tar
baseset/opengfx2_%.tar: baseset/opengfx2_%.obg README.md LICENSE CHANGELOG.md baseset/ogfx2c_arctic_%.grf baseset/ogfx2e_extra_%.grf baseset/ogfx2h_tropical_%.grf baseset/ogfx2i_logos_%.grf baseset/ogfx2t_toyland_%.grf baseset/ogfx21_base_%.grf baseset/ogfx2c_arctic_%.md5 baseset/ogfx2e_extra_%.md5 baseset/ogfx2h_tropical_%.md5 baseset/ogfx2i_logos_%.md5 baseset/ogfx2t_toyland_%.md5 baseset/ogfx21_base_%.md5
	$(eval TMP=$(word 2, $(subst _, ,$(basename $(notdir $@)))))
	mkdir -p baseset/opengfx2_$(TMP)
	cp README.md baseset/opengfx2_$(TMP)/readme.md
	cp LICENSE baseset/opengfx2_$(TMP)/license.txt
	cp CHANGELOG.md baseset/opengfx2_$(TMP)/changelog.md
	cp baseset/*_$(TMP).grf baseset/opengfx2_$(TMP)/
	cp baseset/opengfx2_$(TMP).obg baseset/opengfx2_$(TMP)/
	cd baseset && tar -cf opengfx2_$(TMP).tar opengfx2_$(TMP)/
	rm -r baseset/opengfx2_$(TMP)

# OBG for baseset
# FORCE, as baseset_generate_obg check for necessary updates
.PRECIOUS: baseset/opengfx2_%.obg
baseset/opengfx2_%.obg: baseset/ogfx2c_arctic_%.grf baseset/ogfx2e_extra_%.grf baseset/ogfx2h_tropical_%.grf baseset/ogfx2i_logos_%.grf baseset/ogfx2t_toyland_%.grf baseset/ogfx21_base_%.grf baseset/ogfx2c_arctic_%.md5 baseset/ogfx2e_extra_%.md5 baseset/ogfx2h_tropical_%.md5 baseset/ogfx2i_logos_%.md5 baseset/ogfx2t_toyland_%.md5 baseset/ogfx21_base_%.md5 baseset/baseset_generate_obg.py baseset/lang/*.lng
	$(eval TMP=$(word 2, $(subst _, ,$(basename $(notdir $@)))))
	python3 baseset/baseset_generate_obg.py $(TMP) baseset/

# GRF and MD5 for baseset
.PRECIOUS: baseset/%.grf baseset/%.md5
baseset/%.grf: baseset/%.nml graphics_4.tmp baseset/lang/*.lng
	cd baseset && nmlc -p DOS --quiet -c $(notdir $<) --md5 $(basename $(notdir $<)).md5

#baseset/%.md5: baseset/%.nml graphics
#	cd baseset && nmlc -p DOS --quiet -c $(notdir $<) --md5 $(basename $(notdir $<)).md5

# NML for baseset
# FORCE, as nml_preprocessor.py will check if updates are necessary
# TODO: Use variables/parameters somehow to avoid duplication
.PRECIOUS: baseset/%_8.nml
baseset/%_8.nml: baseset/%.pnml templates/nml_preprocessor.py FORCE
	$(eval TMP=$(word 3, $(subst _, ,$(basename $(notdir $@)))))
	python3 templates/nml_preprocessor.py $< $(TMP)

.PRECIOUS: baseset/%_8ez.nml
baseset/%_8ez.nml: baseset/%.pnml templates/nml_preprocessor.py FORCE
	$(eval TMP=$(word 3, $(subst _, ,$(basename $(notdir $@)))))
	python3 templates/nml_preprocessor.py $< $(TMP)

.PRECIOUS: baseset/%_32.nml
baseset/%_32.nml: baseset/%.pnml templates/nml_preprocessor.py FORCE
	$(eval TMP=$(word 3, $(subst _, ,$(basename $(notdir $@)))))
	python3 templates/nml_preprocessor.py $< $(TMP)

.PRECIOUS: baseset/%_32ez.nml
baseset/%_32ez.nml: baseset/%.pnml templates/nml_preprocessor.py FORCE
	$(eval TMP=$(word 3, $(subst _, ,$(basename $(notdir $@)))))
	python3 templates/nml_preprocessor.py $< $(TMP)

# Constructs input pnml name from parsing output _-delimited ogfx2<basestr>_<basename>_<nmltype>.nml name
#.PRECIOUS: baseset/%.nml
#baseset/%.nml: baseset/$(word 1, $(subst _, ,$(basename $(notdir $<))))_$(word 2, $(subst _, ,$(basename $(notdir $<)))).pnml templates/nml_preprocessor.py FORCE
#	$(eval TMP=$(word 3, $(subst _, ,$(basename $(notdir $@)))))
#	python3 templates/nml_preprocessor.py $< $(TMP)

# NewGRFs
.PNONY: newgrf
newgrf: newgrf/ogfx2_landscape.grf newgrf/ogfx2_objects.grf newgrf/ogfx2_settings.grf newgrf/ogfx2_stations.grf newgrf/ogfx2_trees.grf newgrf/ogfx2_trams.grf newgrf/ogfx2_trains.grf

# GRF for NewGRFs
.PRECIOUS: newgrf/ogfx2_%.grf
newgrf/ogfx2_%.grf: newgrf/ogfx2_%.nml graphics_4.tmp newgrf/lang/%/*.lng
	$(eval TMP=$(word 2, $(subst _, ,$(basename $(notdir $@)))))
	cd newgrf && nmlc -p DOS --quiet -c -l lang/$(TMP) $(notdir $<)

# NML for NewGRFs
.PRECIOUS: newgrf/ogfx2_%.nml FORCE
newgrf/ogfx2_%.nml: newgrf/ogfx2_%.pnml templates/nml_preprocessor.py FORCE
	python3 templates/nml_preprocessor.py $< 32ez exclude_name_suffix

# Graphics
# Python generation of all graphics from PNG sources
dependencies: dependencies.tmp

.PRECIOUS: dependencies.tmp
dependencies.tmp:
	python3 install_dependencies.py
	python3 -m pip freeze > dependencies.tmp

clean_dependencies:
	rm -f dependencies.tmp

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
	$(eval TMP=$(word 2, $(subst _, ,$(basename $(notdir $@)))))
	python3 graphics/generate_graphics.py $(TMP)

# Get font git dependencies
graphics/fonts/openttd-ttf:
	cd graphics/fonts && git clone https://github.com/OpenTTD/OpenTTD-TTF

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
