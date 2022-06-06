__author__ = 'Pietro Rando Mazzarino'
__date__ = '2022/06/03'
__credits__ = ['Pietro Rando Mazzarino']
__email__ = 'pietro.randomazzarino@polito.it'

#this script does what its done in omc_backend.test_teaser_backend.py
from omc_backend.test_project import Project # the version of project we are going to use instead of the one from teaser
from omc_backend.test_teaser_backend import generate_archetype, export_ibpsa
import pandas as pd
from OMPython import OMCSessionZMQ
from OMPython import ModelicaSystem
import numpy as np




''' IF USING PROJECT FROM DANIELE ADD EXTENSION FOR FMU AND NEW TEMPLATES FOR THERMAL MODEL
INPUT WEATHER CHECK THE OTHERS'''
prj = Project()
prj.name = 'test_thesis'

models_path = '/TeaserOut/modelica/ibpsa'
dict_building = {
        'id': [0],
        'type': ['residential'],
        'method': ['iwu'],
        'usage': ['single_family_dwelling'],
        'name': ["ResidentialBuilding"],
        'year_of_construction': [2010],
        'number_of_floors': [1],
        'height_of_floors': [2.75],
        'net_leased_area': [150]
    }
# dict_building = {
#         'id': [0,1],
#         'type': ['residential','residential'],
#         'method': ['iwu','tabula_dk'],
#         'usage': ['single_family_dwelling', 'apartment_block'],
#         'name': ["ResidentialBuilding", "ApartmentBlock"],
#         'year_of_construction': [2010, 1999],
#         'number_of_floors': [1,4],
#         'height_of_floors': [2.75, 2.75],
#         'net_leased_area': [150, 150]
#     }
db = pd.DataFrame.from_dict(dict_building)
prj = generate_archetype(prj, db)
export_ibpsa(prj,models_path,fmu_io=True) #EXPORTED THE MODELICA IBPSA MODEL OF THE PROJECT


#CONVERT THE MODELICA IBPSA MODELS IN FMUs exploiting OMC methods (Modelica System)
#todo resolve problem with aixlib version and compatibility inside omc
mo_lib = ["Modelica, {\"3.2.2\"}","AixLib"]


mo_name = "test_thesis.ResidentialBuilding.ResidentialBuilding_Models.ResidentialBuilding_SingleDwelling"

mo_fullpath = "/home/pietrorm/Documents/CODE/TEASER/TeaserOut/modelica/ibpsa/test_thesis/package.mo"
#mo_fullpath= '/home/pietrorm/Documents/CODE/TEASER/TeaserOut/modelica/ibpsa/test_thesis/ResidentialBuilding/ResidentialBuilding_Models/ResidentialBuilding_SingleDwelling.mo'

momodel = ModelicaSystem(mo_fullpath, mo_name, mo_lib)
#TODO when exporting fmu ensure compatibility with linux platform
momodel.convertMo2Fmu(version="2.0", fmuType="cs",fileNamePrefix='RC_building')

#test not using modelcia system
# omc = OMCSessionZMQ()
#
# omc.sendExpression("getVersion()")
#
# omc.sendExpression("loadModel(Modelica, {\"3.2.3\"})") # load System Library
#
# omc.sendExpression("loadModel(AixLib)") # load System Library
# #omc.sendExpression("loadModel(Buildings,{\"7.0.0\"})")
#
# omc.sendExpression(f"loadFile(/home/pietrorm/Documents/CODE/TEASER/TeaserOut/modelica/ibpsa/test_thesis/package.mo)")
# #%%
# omc.sendExpression("getClassNames()") # get Classes loaded
#
# #%%
# omc.sendExpression("isModel(Building.ResidentialBuilding.ResidentialBuilding_Models.ResidentialBuilding_SingleDwelling)")
#
# #%%
# omc.sendExpression("checkModel(Building.ResidentialBuilding.ResidentialBuilding_Models.ResidentialBuilding_SingleDwelling)")
#
# #%%
# omc.sendExpression("translateModelFMU(Building.ResidentialBuilding.ResidentialBuilding_Models.ResidentialBuilding_SingleDwelling)")
#
