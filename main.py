__author__ = 'Pietro Rando Mazzarino'
__date__ = '2022/06/03'
__credits__ = ['Pietro Rando Mazzarino']
__email__ = 'pietro.randomazzarino@polito.it'

from Prj_creation_archetypes import PrjScenario as Prj
from utils import read_config



#this dict should be the outcome of the GIS processing
#the lists contains the molteplicity of buildings
dict_building = {
        'id': [0,1],
        'type': ['residential','residential'],
        'method': ['tabula_dk','tabula_dk'],
        'usage': ['apartment_block', 'apartment_block'],
        'name': ["Bui01", "Bui02",],
        'year_of_construction': [2010, 1999],
        'number_of_floors': [1,2],
        'height_of_floors': [2.75, 2.75],
        'net_leased_area': [150, 150],
        'with_ahu':[False,False],
        'internal_gains_mode':[1,1],
        'residential_layout':[None,None],
        'neighbour_buildings':[None,None],
        'attic':[None,None],
        'cellar':[None,None],
        'dormer':[None,None],
        'construction_type':['tabula_standard','tabula_standard'],
        'number_of_apartments':[None, None],
    }

#config file
config = read_config('config.yaml')
prj_name='newPRjclass_test'
project = Prj(config,prj_name)
print(project)
project.create_buildings_from_input(dict_building)
print(project)
#NB this method if None or nothing is passed uses values from config except for the weather for which takes the one from teaser
project.export_modelica(weather=None, n_el=None, model=None,library=None, single_bui = None, template=None, fmu_io=None)
print(project)

