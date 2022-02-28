"""Test the possibility to perform stepped simulation of modelica model through OMPython
"""

from OMPython import ModelicaSystem
import numpy as np



def dict_to_list(dict):
    list = []
    for attr, value in dict.items():
        list.append(f'{attr}={value}')
    return list



# %%
mo_lib = ["Modelica, {\"3.2.3\"}", "AixLib", "/home/pietrorm/Documents/CODE/TEASER/TeaserOut/modelica/packages/Ideal_HeaterCooler_RC2.mo" ]
mo_name = "Residential_test.ResidentialApartmentBlock_1.ResidentialApartmentBlock_1_Models.ResidentialApartmentBlock_1_SingleDwelling"
mo_path = "/home/pietrorm/Documents/CODE/TEASER/TeaserOut/modelica/Residential_test/package.mo"
dummy = ModelicaSystem(mo_path, mo_name, mo_lib)

# %%
startTime = 0

stepSize = 1

stopTime = 3

nsteps = np.arange(startTime, stopTime, stepSize)

# %% Stepped simulation
res = []
for time in nsteps:
    simopt = dummy.getSimulationOptions()
    simopt['startTime'] = time
    simopt['stopTime'] = time + stepSize
    simopt['stepSize'] = stepSize
    dummy.setSimulationOptions(dict_to_list(simopt))
    dummy.simulate()
    #print(dummy.getOutputs())
    res.append(dummy.getOutputs())
    print(dummy.getSolutions(list(dummy.outputlist.keys())))


# %% Complete Simulation
# simopt = {'startTime': str(startTime),
#           'stopTime': str(stopTime),
#           'stepSize': str(stepSize),
#           'tolerance': '1e-06',
#           'solver': 'dassl'}
#
# dummy.setSimulationOptions(dict_to_list(simopt))
# dummy.simulate()


# %%

