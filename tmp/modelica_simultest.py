from OMPython import ModelicaSystem
import numpy as np



def dict_to_list(dict):
    list = []
    for attr, value in dict.items():
        list.append(f'{attr}={value}')
    return list


mo_lib = ["Modelica, {\"3.2.2\"}","AixLib"]

#mo_name if the project has more models must contains the path with dots
mo_name = "test_thesis.ResidentialBuilding.ResidentialBuilding_Models.ResidentialBuilding_SingleDwelling"

mo_fullpath = "/home/pietrorm/Documents/CODE/TEASER/TeaserOut/modelica/ibpsa/test_thesis/package.mo"

# %%
model = ModelicaSystem(mo_fullpath,mo_name,mo_lib)
# %%
startTime = 0

stepSize = 3600

stopTime = 100 * 3600

nsteps = np.arange(startTime, stopTime, stepSize)

# %% Stepped simulation
res = []
for time in nsteps:
    simopt = model.getSimulationOptions()
    simopt['startTime'] = time
    simopt['stopTime'] = time + stepSize
    simopt['stepSize'] = stepSize
    model.setSimulationOptions(dict_to_list(simopt))
    model.simulate()
    #print(dummy.getOutputs())
    res.append(model.getOutputs())
    print(model.getSolutions(list(model.outputlist.keys())))

print (res)