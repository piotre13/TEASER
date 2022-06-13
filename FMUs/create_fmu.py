__author__ = 'Pietro Rando Mazzarino'
__date__ = '2022/06/03'
__credits__ = ['Pietro Rando Mazzarino']
__email__ = 'pietro.randomazzarino@polito.it'


from OMPython import ModelicaSystem
import os
import json
from sys import argv

#TODO authomated extraction of FMU's for each different bulding in teaser modelica project
#fmu extraction of single building with option possibility
def Modelica2FMU (mo_name, mo_path, mo_lib, FMU_name,FMU_version="2.0", FMU_type = "cs",
                  FMU_folder="/home/pietrorm/Documents/CODE/TEASER/FMUs",commandLineOptions=None, **kwargs):
    #'--fmiFlags = s:cvode' '--fmiFilter:none'
    #momodel = ModelicaSystem(mo_path, mo_name, mo_lib, '--fmiFlags=s:cvode')
    # instantiating the model and building it
    momodel = ModelicaSystem(mo_path, mo_name, mo_lib, commandLineOptions=commandLineOptions)
    files = os.listdir()
    momodel.buildModel()

    # setting the options/params and inputs if present
    if kwargs:
        for key in kwargs:
            if key == 'set_params':
                momodel.setParameters(kwargs[key])
            elif key == 'set_continous':
                momodel.setContinuous(kwargs[key])
            elif key == 'set_simOptions':
                momodel.setSimulationOptions(kwargs[key])
            elif key == 'set_linearOptions':
                momodel.setLinearizationOptions(kwargs[key])
            elif key == 'set_optOptions':
                momodel.setOptimizationOptions(kwargs[key])
            elif key == 'set_inputs':
                momodel.setInputs(kwargs[key])

    # creating FMU description
    description = {'quantities': momodel.getQuantities(),
                   'continous': momodel.getContinuous(),
                   'params': momodel.getParameters(),
                   #'linear_params': momodel.getlinearParameters(),
                   'inputs': momodel.getInputs(),
                   'outputs': momodel.getOutputs(),
                   'sim_options': momodel.getSimulationOptions(),
                   'lin_options': momodel.getLinearizationOptions(),
                   'opt_options': momodel.getOptimizationOptions(),
                   #'solutions': momodel.getSolutions()#could not work without simulate}
                    }

    # create & extract the FMU
    fmu = momodel.convertMo2Fmu(version=FMU_version, fmuType= FMU_type, fileNamePrefix= FMU_name, includeResources=True)

    #clear the folder:
    files = [f for f in os.listdir(FMU_folder) if os.path.isfile(f)]
    acc_ext = ['.py','.fmu','.md']
    for file in files:
        if not any([file.endswith(i) for i in acc_ext]):
            file = os.path.join(FMU_folder,file)
            os.remove(file)

    #save the description file
    path = 'description_json/'+FMU_name+'.json'
    with open(path, 'w') as fp:
        json.dump(description, fp, sort_keys=True, indent=4)

    return fmu, description




if __name__ == '__main__':
    #mo_lib = ["Modelica, {\"3.2.3\"}", "AixLib, {\"0.9.1\"}", "/home/pietrorm/Documents/CODE/TEASER/TeaserOut/modelica/packages/Ideal_HeaterCooler_RC2.mo" ]
    mo_lib = ["Modelica, {\"3.2.3\"}", "AixLib",] #"/home/pietrorm/Documents/CODE/TEASER/FMUs/Building2/package.mo" ]

    # mo_name if the project has more models must contains the path with dots
    #mo_name = "Residential_test.ResidentialApartmentBlock_1.ResidentialApartmentBlock_1_Models.ResidentialApartmentBlock_1_SingleDwelling"
    #mo_name = "Building.ResidentialBuilding.ResidentialBuilding_Models.ResidentialBuilding_SingleDwelling"
    mo_name = "ApartmentBlock_DE.Bui04.Bui04_Models.Bui04_SingleDwelling"

    #mo_name = "RC_IdealHeatCool"

    #mo_fullpath = "/home/pietrorm/Documents/CODE/TEASER/FMUs/Building/package.mo"
    mo_fullpath="/home/pietrorm/Documents/CODE/TEASER/TeaserOut/modelica/ApartmentBlock_DE/package.mo"

    kwargs = {'set_params':[],'set_continous':[],'set_simOptions':[], 'set_linearOptions':[], 'set_optOptions':[], 'set_inputs':[],}

    Modelica2FMU(mo_name, mo_fullpath, mo_lib, 'Bui04_DE', "2.0")