from OMPython import ModelicaSystem



#todo ask daniele what he does

def Modelica2FMU (mo_name, mo_path, mo_lib, FMU_name,FMU_version="2.0", FMU_type = "cs"):
    momodel = ModelicaSystem(mo_path, mo_name, mo_lib)
    fmu = momodel.convertMo2Fmu(version=FMU_version, fmuType= FMU_type, fileNamePrefix= FMU_name)
    return fmu




if __name__ == '__main__':
    mo_lib = ["Modelica, {\"3.2.2\"}", "AixLib"]
    # mo_name if the project has more models must contains the path with dots
    mo_name = "test_thesis.ResidentialBuilding.ResidentialBuilding_Models.ResidentialBuilding_SingleDwelling"
    mo_fullpath = "/home/pietrorm/Documents/CODE/TEASER/TeaserOut/modelica/ibpsa/test_thesis/package.mo"

    Modelica2FMU(mo_name, mo_fullpath, mo_lib, 'RC_building', "2.0")