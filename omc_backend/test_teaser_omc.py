
"""Teaser omc.

_author_: Daniele Schiera daniele.schiera@polito.it
"""
from test_teaser_backend import *
import pandas as pd
from OMPython import OMCSessionZMQ




#%% Example of buildings dictionary
dict_building = {
    'i': [0],
    'type': ['residential'],
    'method':['iwu'],
    'usage':['single_family_dwelling'],
    'name':["ResidentialBuilding"],
    'year_of_construction':[1988],
    'number_of_floors':[2],
    'height_of_floors':[3.2],
    'net_leased_area':[200]
}

#%%
db = pd.DataFrame.from_dict(dict_building)
prj = generate_archetype('Building', db)
om_models_dir = r"/models/openmodelica"
export_ibpsa(prj,om_models_dir)

#%% OpenModelica Compiler Session

omc = OMCSessionZMQ()

omc.sendExpression("getVersion()")

omc.sendExpression("loadModel(Modelica, {\"3.2.3\"})") # load System Library

omc.sendExpression("loadModel(AixLib)") # load System Library
#omc.sendExpression("loadModel(Buildings,{\"7.0.0\"})")

omc.sendExpression(f"loadFile(\"{om_models_dir}/Building/package.mo\")")
#%%
omc.sendExpression("getClassNames()") # get Classes loaded

#%%
omc.sendExpression("isModel(Building.ResidentialBuilding.ResidentialBuilding_Models.ResidentialBuilding_SingleDwelling)")

#%%
omc.sendExpression("checkModel(Building.ResidentialBuilding.ResidentialBuilding_Models.ResidentialBuilding_SingleDwelling)")

#%%
omc.sendExpression("translateModelFMU(Building.ResidentialBuilding.ResidentialBuilding_Models.ResidentialBuilding_SingleDwelling)")



