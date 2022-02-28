from OMPython import ModelicaSystem
from sys import argv


def Modelica2FMU (mo_name, mo_path, mo_lib, FMU_name,FMU_version="2.0", FMU_type = "me_cs"):

    momodel = ModelicaSystem(mo_path, mo_name, mo_lib)
    sim_opt = momodel.getSimulationOptions()
    sim_opt['solver']= 'cvode'
    sim_opt['stepSize'] = '1'
    momodel.setSimulationOptions(sim_opt)
    log = momodel.getconn.sendExpression("getErrorString()")
    #print(sim_opt)

    #momodel.simulationFlag = True
    fmu = momodel.convertMo2Fmu(version=FMU_version, fmuType= FMU_type, fileNamePrefix= FMU_name, includeResources=True)
    return fmu, log




if __name__ == '__main__':
    mo_lib = ["Modelica, {\"3.2.3\"}", "AixLib", "/home/pietrorm/Documents/CODE/TEASER/TeaserOut/modelica/packages/Ideal_HeaterCooler_RC2.mo" ]
    # mo_name if the project has more models must contains the path with dots
    mo_name = "Residential_test.ResidentialApartmentBlock_1.ResidentialApartmentBlock_1_Models.ResidentialApartmentBlock_1_SingleDwelling"
    mo_fullpath = "/home/pietrorm/Documents/CODE/TEASER/TeaserOut/modelica/Residential_test/package.mo"

    Modelica2FMU(mo_name, mo_fullpath, mo_lib, 'RC_building_HeatCool', "2.0")