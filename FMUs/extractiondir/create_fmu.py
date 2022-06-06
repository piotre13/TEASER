from OMPython import ModelicaSystem
from sys import argv


def Modelica2FMU (mo_name, mo_path, mo_lib, FMU_name,FMU_version="2.0", FMU_type = "cs"):
    #'--fmiFlags = s:cvode' '--fmiFilter:none'
    #momodel = ModelicaSystem(mo_path, mo_name, mo_lib, '--fmiFlags=s:cvode')
    momodel = ModelicaSystem(mo_path, mo_name, mo_lib, commandLineOptions='--fmiFlags=s:cvode')
    momodel.buildModel()
    momodel.sendExpression("setCommandLineOptions(","\"",,"\"",")")
    print(momodel.getQuantities("h_heater"))
    print(momodel.getParameters("h_heater"))

    sim_opt = momodel.getSimulationOptions()
    #momodel.paramlist['h_heater']= 1000.0
    momodel.setParameters(["heaterCoolerController.zoneParam.hHeat=1000","heaterCooler.zoneParam.hHeat=1000","h_heater=1000"])

    #'heaterCoolerController.zoneParam.hHeat', 'heaterCooler.zoneParam.hHeat', 'h_heater'
    #sim_opt['solver']= 'cvode'
    #sim_opt['stepSize'] = '10'
    #momodel.setSimulationOptions(sim_opt)
    #momodel.setLinearizationOptions(["startTime=0.0","stepSize=900","stopTime=86400.0","tolerance=1e-08"])
    #{'startTime': 0.0, 'stopTime': 100000000, 'numberOfIntervals': 500, 'stepSize': 900, 'tolerance': 1e-08}
    log = momodel.getconn.sendExpression("getErrorString()")
    #momodel.buildModel()
    print(momodel.getParameters('h_heater'))
    print(momodel.getQuantities("h_heater"))

    #print(sim_opt)

    #momodel.simulationFlag = True
    fmu = momodel.convertMo2Fmu(version=FMU_version, fmuType= FMU_type, fileNamePrefix= FMU_name, includeResources=False)
    return fmu, log




if __name__ == '__main__':
    #mo_lib = ["Modelica, {\"3.2.3\"}", "AixLib, {\"0.9.1\"}", "/home/pietrorm/Documents/CODE/TEASER/TeaserOut/modelica/packages/Ideal_HeaterCooler_RC2.mo" ]
    mo_lib = ["Modelica, {\"3.2.3\"}", "AixLib",] #"/home/pietrorm/Documents/CODE/TEASER/FMUs/Building2/package.mo" ]

    # mo_name if the project has more models must contains the path with dots
    #mo_name = "Residential_test.ResidentialApartmentBlock_1.ResidentialApartmentBlock_1_Models.ResidentialApartmentBlock_1_SingleDwelling"
    mo_name = "Building.ResidentialBuilding.ResidentialBuilding_Models.ResidentialBuilding_SingleDwelling"

    #mo_name = "RC_IdealHeatCool"

    mo_fullpath = "/home/pietrorm/Documents/CODE/TEASER/FMUs/Building/package.mo"

    Modelica2FMU(mo_name, mo_fullpath, mo_lib, 'Building_CVODEtestExtraction', "2.0")