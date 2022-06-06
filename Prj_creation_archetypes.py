__author__ = 'Pietro Rando Mazzarino'
__date__ = '2022/06/03'
__credits__ = ['Pietro Rando Mazzarino']
__email__ = 'pietro.randomazzarino@polito.it'



#from teaser.project import Project
from teaser_modified.project import Project
import teaser.logic.utilities as utilities
import yaml
import os
import pickle

'''this is old script using a class maybe i'll only use functions it's cleaner'''

class PrjScenario():

    def __init__(self, config, prj_name ):
        self.config = config
        self.name = prj_name
        self.prj = Project()
        self.prj.name = self.name
        self.prj.weather_file_path = config['paths']['weather_data']
        self.set_modelica_info()

        # CREATE project folder
        self.create_prj_folder() #creating the folder if first time

    def set_modelica_info(self):
        #todo expand to other modelica info
        self.prj.modelica_info.current_solver = self.config['modelica_info']['current_solver']


    def create_buildings_from_input(self, building_dict):
        assert (len(building_dict['id']) == len(building_dict[i]) for i in building_dict) , "Number of buildings info and number of buildings is NOT matching!\n"
        for i in range(len(building_dict['id'])):

            if building_dict['type'][i] == 'residential':
                self.prj.add_residential(
                    method= building_dict['method'][i],
                    usage= building_dict['usage'][i],
                    name= building_dict['name'][i],
                    year_of_construction= building_dict['year_of_construction'][i],
                    number_of_floors= building_dict['number_of_floors'][i],
                    height_of_floors= building_dict['height_of_floors'][i],
                    net_leased_area= building_dict['net_leased_area'][i],
                    with_ahu= building_dict['with_ahu'][i],
                    internal_gains_mode= building_dict['internal_gains_mode'][i],
                    residential_layout= building_dict['residential_layout'][i],
                    neighbour_buildings= building_dict['neighbour_buildings'][i],
                    attic= building_dict['attic'][i],
                    cellar= building_dict['cellar'][i],
                    dormer= building_dict['dormer'][i],
                    construction_type= building_dict['construction_type'][i],
                    number_of_apartments= building_dict['number_of_apartments'][i])

            elif building_dict['type'][i] == 'non_residential':
                self.prj.add_non_residential(
                    method=building_dict['method'][i],
                    usage=building_dict['usage'][i],
                    name=building_dict['name'][i],
                    year_of_construction=building_dict['year_of_construction'][i],
                    number_of_floors=building_dict['number_of_floors'][i],
                    height_of_floors=building_dict['height_of_floors'][i],
                    net_leased_area=building_dict['net_leased_area'][i],
                    with_ahu=building_dict['with_ahu'][i],
                    internal_gains_mode=building_dict['internal_gains_mode'][i],
                    residential_layout=building_dict['residential_layout'][i],
                    neighbour_buildings=building_dict['neighbour_buildings'][i],
                    attic=building_dict['attic'][i],
                    cellar=building_dict['cellar'][i],
                    dormer=building_dict['dormer'][i],
                    construction_type=building_dict['construction_type'][i],
                    number_of_apartments=building_dict['number_of_apartments'][i])

            else:
                print('Unknown Building type!')

    def create_from_shp(self, shp_file):
        building_dict ={}
        #TODO create a scenario from shapefile
        return building_dict


    def export_modelica(self, weather=None, n_el=None, model=None,library=None, single_bui = None, template=None, fmu_io=None):
        '''library for IBPSA export has to be 'AixLib',
            'Buildings', 'BuildingSystems' or 'IDEAS'
            the export with export_ailib works only on dymola!!!
            NB for the parameters there are 2 possibilities to pass them while using the method or alternatively to modify them in config file
            parameters from config are used IF and ONLY IF the passed parameters are None'''
        n_el = self.config['export_modelica']['n_el'] if n_el == None else n_el
        model = self.config['export_modelica']['model'] if model == None else model
        library = self.config['export_modelica']['library'] if library == None else library
        template = self.config['paths']['modelica_template'] if template == None else template
        fmu_io = self.config['export_modelica']['fmu_io'] if fmu_io==None else fmu_io
        single_bui = self.config['export_modelica']['single_bui'] if single_bui==None else single_bui
        #todo understand how to deal with weather file
        if model == 'IBPSA':
            self.prj.used_library_calc = 'IBPSA'
            self.prj.number_of_elements_calc = n_el
            self.prj.merge_windows_calc = False
            if weather == None:
                self.prj.weather_file_path = utilities.get_full_path(os.path.join(
                    "data",
                    "input",
                    "inputdata",
                    "weatherdata",
                    "DEU_BW_Mannheim_107290_TRY2010_12_Jahr_BBSR.mos"))
            else:
                self.prj.weather_file_path = weather
            try: # to check parameters
                self.prj.calc_all_buildings(raise_errors=True)
            except:
                raise ValueError('Parameters for modelica model are not ok!')

            path = self.config['paths']['modelica_out']
            self.prj.export_ibpsa(
                    library=library,
                    internal_id=single_bui,
                    path=path,
                    fmu_io=fmu_io,
                    template_path=template
                    )

        #TODO multizone export is work in progress

        # elif model == 'MULTIZONE': # NB NOT USED JUST FOR FURTHER DEVELOPMENT
        #     self.prj.used_library_calc = 'AixLib'
        #     self.prj.number_of_elements_calc = n_el
        #     if weather == None:
        #         self.prj.weather_file_path = utilities.get_full_path(os.path.join(
        #                                                                     "data",
        #                                                                     "input",
        #                                                                     "inputdata",
        #                                                                     "weatherdata",
        #                                                                     "DEU_BW_Mannheim_107290_TRY2010_12_Jahr_BBSR.mos"))
        #
        #     else:
        #         self.prj.weather_file_path = weather
        #     try: # to check parameters
        #         self.prj.calc_all_buildings(raise_errors=True)
        #     except:
        #         raise ValueError('Parameters for modelica model are not ok!')
        #
        #     path = self.config['folder_modelica_path']
        #     self.prj.export_aixlib(building_model=None,
        #                             zone_model=None,
        #                             corG=None,
        #                             internal_id=None,
        #                             path=path,
        #                             fmu_io=True,
        #                             template_path=self.config['template_multizone'])
        #
        else:
            raise ValueError('Unknown or Unsupported model: %s'%model)



    def auto_retrofit_all(self):

        self.prj.retrofit_all_buildings(
            year_of_retrofit = self.config['retrofit_params']['year'],
            type_of_retrofit = self.config['retrofit_params']['type_of_retrofit'],
            window_type = self.config['retrofit_params']['window_type'],
            material = self.config['retrofit_params']['material'])


    def save_project(self, mode='json'):
        prj_path = os.path.join(self.config['paths']['teaser_project_out'], self.name)

        if mode == 'json':
            self.prj.save_project(file_name=self.name,path=prj_path)
        elif mode == 'pickle':
            pickle_file = self.name + '.p'
            pickle_path = os.path.join(prj_path,pickle_file)
            pickle.dump(self.prj, open(pickle_path, "wb"))
        else:
            raise ValueError('Unknown saving format: "%s"' % mode)

    def load_project(self, path):
        if path.endswith('.json'):
            self.prj.load_project(path=path)
        elif path.endswith('.p'):
            self.prj = pickle.load(open(path, "rb"))
        else:
            raise ValueError('Unknown format : %s' % path)

        pass

    def create_prj_folder(self):
        path = os.path.join(self.config['paths']['teaser_project_out'],self.name)
        if not os.path.exists(path):
            utilities.create_path(path)
        else:
            pass




def read_config(path):
    stream = open(path, 'r')
    dictionary = yaml.load(stream,Loader=yaml.FullLoader)
    return dictionary

# residential_dict = {
#
#     "ResidentialApartmentBlock_1"  :   {
#         'method' : 'tabula_de',  # could be tabula_dk
#         'usage' : 'apartment_block',
#         'year_of_construction' : 1970,
#         'number_of_floors' : 5,
#         'height_of_floors' : 3.2,
#         'net_leased_area' : 280,
#         'construction_type' : 'tabula_standard',
#         'with_ahu':False,
#         'internal_gains_mode':3} ,
#
#     "ResidentialApartmentBlock_2" :    {
#         'method' : 'tabula_de',  # could be tabula_dk
#         'usage' : 'apartment_block',
#         'year_of_construction' : 1970,
#         'number_of_floors' : 5,
#         'height_of_floors' : 3.2,
#         'net_leased_area' : 280,
#         'construction_type' : 'tabula_standard',
#         'with_ahu':False,
#         'internal_gains_mode':3},
#
# }



#if __name__ == '__main__':
    #config = read_config('config.yaml')
    #prj_name = 'MultiZone_test'
    #instantiate the scenario project class
    #PrJ = PrjScenario(config, prj_name)
    #PrJ.create_buildings(residential_dict)
    #PrJ.export_modelica(weather=None, n_el=2, model='MULTIZONE',library= 'AixLib', single_bui = None)
    #PrJ.convert2FMU()
    #PrJ.save_project('pickle')
