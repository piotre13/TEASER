from OMPython import ModelicaSystem


mo_lib = ["Modelica, {\"3.2.2\"}","AixLib"]

#mo_name if the project has more models must contains the path with dots
mo_name = "test_thesis.ResidentialBuilding.ResidentialBuilding_Models.ResidentialBuilding_SingleDwelling"

mo_fullpath = "/home/pietrorm/Documents/CODE/TEASER/TeaserOut/modelica/ibpsa/test_thesis/package.mo"
#mo_fullpath= '/home/pietrorm/Documents/CODE/TEASER/TeaserOut/modelica/ibpsa/test_thesis/ResidentialBuilding/ResidentialBuilding_Models/ResidentialBuilding_SingleDwelling.mo'

momodel = ModelicaSystem(mo_fullpath, mo_name, mo_lib)
#TODO when exporting fmu ensure compatibility with linux platform
momodel.convertMo2Fmu(version="2.0", fmuType="cs",fileNamePrefix='RC_building')