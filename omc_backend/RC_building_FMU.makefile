# FIXME: before you push into master...
RUNTIMEDIR=C:/Program Files/OpenModelica1.18.0-64bit/include/omc/c/
#COPY_RUNTIMEFILES=$(FMI_ME_OBJS:%= && (OMCFILE=% && cp $(RUNTIMEDIR)/$$OMCFILE.c $$OMCFILE.c))

fmu:
	rm -f RC_building.fmutmp/sources/RC_building_init.xml
	cp -a "C:/Program Files/OpenModelica1.18.0-64bit/share/omc/runtime/c/fmi/buildproject/"* RC_building.fmutmp/sources
	cp -a RC_building_FMU.libs RC_building.fmutmp/sources/

