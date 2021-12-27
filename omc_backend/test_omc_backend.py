"""Test the possibility to perform stepped simulation of modelica model through OMPython or also extra FMU after
modification of Modelica model


_author_: Daniele Schiera daniele.schiera@polito.it
"""

from OMPython import ModelicaSystem
import numpy as np


def dict_to_list(dict):
    list = []
    for attr, value in dict.items():
        list.append(f'{attr}={value}')
    return list


mo_libraries = ["Modelica, {\"3.2.3\"}","AixLib"]##"Buildings, {\"7.0.0\"}"] #"AixLib"]#, {\"0.9.1\"}"]
# La libreria Aixlib 1.0.0 sembra non funzionare bene per esprotare l'fmu (non la zippa ed ottengo solo un <nome>.fmutmp
#%%
mo_name = "Building.ResidentialBuilding.ResidentialBuilding_Models.ResidentialBuilding_SingleDwelling"

mo_fullpath = "D:/Projects/PycharmProjects/casestudy/models/openmodelica/Building/package.mo"

momodel = ModelicaSystem(mo_fullpath, mo_name, mo_libraries)

#momodel.getconn.sendExpression("setCommandLineOptions(\"-d=newInst --fmiFlags=s:cvode\")") # non funziona

momodel.convertMo2Fmu(version="2.0", fmuType="cs",fileNamePrefix='RC_building')

log = momodel.getconn.sendExpression("getErrorString()")
print('Done')

#%%
#
# mo_name = "test"
#
# mo_fullpath = "D:/Projects/PycharmProjects/casestudy/uesa/resources/modelica_data/test.mo"
#
# momodel = ModelicaSystem(mo_fullpath, mo_name, mo_libraries)
#
# #momodel.convertMo2Fmu(version="2.0", fmuType="cs")