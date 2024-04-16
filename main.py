__author__ = 'Pietro Rando Mazzarino'
__date__ = '2022/06/03'
__credits__ = ['Pietro Rando Mazzarino']
__email__ = 'pietro.randomazzarino@polito.it'

from Prj_creation_archetypes import PrjScenario as Prj
from utils import read_config
from ZoneSelector import Zone
import time


#********** GIS PROCESSING **************


#this dict should be the outcome of the GIS processing
#the lists contains the molteplicity of buildings
# dict_building = {
#         'id': [0,1,2,3,4,5,6,7],
#         'type': ['residential','residential','residential','residential','residential','residential','residential','residential'],
#         'method': ['tabula_de','tabula_de','tabula_de','tabula_de','tabula_de','tabula_de','tabula_de','tabula_de'],
#         'usage': ['apartment_block', 'apartment_block', 'apartment_block', 'apartment_block', 'apartment_block', 'apartment_block', 'apartment_block', 'apartment_block'],
#         'name': ["Bui01", "Bui02", "Bui03", "Bui04", "Bui05", "Bui06", "Bui07", "Bui08"],
#         'year_of_construction': [1915,1925,1955,1965,1965,1975,1975,1975],
#         'number_of_floors': [3,4,4,5,7,5,8,5],
#         'height_of_floors': [2.75, 2.75, 2.75, 2.75, 2.75, 2.75, 2.75, 2.75],
#         'net_leased_area': [830, 1400, 1600, 3800, 11000, 3300, 19000, 3000],
#         'with_ahu':[False, False, False, False, False, False, False, False],
#         'internal_gains_mode':[1,1,1,1,1,1,1,1],
#         'residential_layout':[None,None,None,None,None,None,None,None],
#         'neighbour_buildings':[None,None,None,None,None,None,None,None],
#         'attic':[None,None,None,None,None,None,None,None],
#         'cellar':[None,None,None,None,None,None,None,None],
#         'dormer':[None,None,None,None,None,None,None,None],
#         'construction_type':[None,None,None,None,None,None,None,None],
#         'number_of_apartments':[None, None, None, None, None, None, None, None],
#     }
#the lists contains the molteplicity of buildings
dict_building = {
        'id': [0],
        'type': ['residential'],
        'method': ['tabula_de'],
        'usage': ['apartment_block'],
        'name': ["Bui01"],
        'year_of_construction': [1967],
        'number_of_floors': [4],
        'height_of_floors': [2.75],
        'net_leased_area': [500],
        'with_ahu':[False],
        'internal_gains_mode':[1],
        'residential_layout':[None],
        'neighbour_buildings':[None],
        'attic':[None],
        'cellar':[None],
        'dormer':[None],
        'construction_type':[None],
        'number_of_apartments':[None],
}
# example_geojson = 'data/_my_data(20).geojson'
# tabula_data = 'data/TABULA_completedataset/TABULA.xlsm'
# istat_census = 'data/R01_11_WGS84/R01_11_WGS84.shp'
#
# z = Zone(example_geojson, tabula_data, 'IT', 'test_paper')
#
# z.get_buildings()
# z.complete_data()
# bui_dict = z.teaser_dict()
# z.plot()
#
#
# #config file
def replicate_experiment(num, dict_building):
	for i in range(num-1):
		for k in dict_building.keys():
			if k == 'id':
				dict_building[k].append(dict_building[k][0]+i+1)
			elif k == 'name':
				dict_building[k].append('Bui0'+str(i+2))
			else:
				dict_building[k].append(dict_building[k][0])
	return dict_building


num= 1
dict_building = replicate_experiment(num, dict_building)



start = time.time()
config = read_config('config.yaml')
prj_name='tabula_ita_test_%s'%num
project = Prj(config,prj_name)
project.create_buildings_from_input(dict_building)
project.save_project()
#NB this method if None or nothing is passed uses values from config except for the weather for which takes the one from teaser
project.export_modelica(weather=None, n_el=None, model=None,library=None, single_bui = None, template=None, fmu_io=None)
end = time.time()

print('Time taken to end the export modelica is: ', end-start)

