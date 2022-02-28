#from teaser.project import Project
from project_new import Project
import teaser.logic.utilities as utilities
from OMPython import ModelicaSystem
import yaml
import os
import pickle
from FMUs.create_fmu import Modelica2FMU

'''this is old script using a class maybe i'll only use functions it's cleaner'''

class PrjScenario(Project):

    def __init__(self, config, prj_name ):
        self.config = config
        self.name = prj_name
        self.prj = Project()
        self.prj.name = self.name
        self.prj.weather_file_path = config['weather_path']
        self.set_modelica_info()

        # CREATE project folder
        self.create_prj_folder() #creating the folder if first time

    def set_modelica_info(self):
        self.prj.modelica_info.current_solver = self.config['modelica_info']['current_solver']


    def create_buildings(self, res_dict = None, non_res_dict = None):
        self.create_residentials(res_dict)
        self.create_non_residentials(non_res_dict)

    def create_residentials(self, res_dict):
        '''info = { num: ,
                    name:,
                    year_of_construction: ,
                    number_of_floors: ,
                    height_of_floors: ,
                    net_leased_area: ,
                    with_ahu: ,
                    internal_gains_mode: ,
                    construction_type: ,
                    } '''
        if res_dict:
            for building, bui_info in res_dict.items():  # ne genero 5
                self.prj.add_residential(
                    method=bui_info['method'], # could be tabula_dk
                    usage=bui_info['usage'],
                    name=building,
                    year_of_construction=bui_info['year_of_construction'],
                    number_of_floors=bui_info['number_of_floors'],
                    height_of_floors=bui_info['height_of_floors'],
                    net_leased_area=bui_info['net_leased_area'],
                    construction_type=bui_info['construction_type'],
                )
        else:
            print('No residential buildings found!')


    def create_non_residentials(self, non_res_dict):
        #todo create non residential for variety
        pass
    def create_from_shp(self, shp_file):
        #TODO create a scenario from shapefile
        pass


    def export_modelica(self, weather=None, n_el=2, model='IBPSA',library= 'AixLib', single_bui = None):
        '''library for IBPSA export has to be 'AixLib',
            'Buildings', 'BuildingSystems' or 'IDEAS'
            the export with export_ailib works only on dymola!!!'''
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

            path = self.config['folder_modelica_path']
            self.prj.export_ibpsa(
                    library=library,
                    internal_id=single_bui,
                    path=path,
                    fmu_io=True,
                    template_path=self.config['template_ibpsa']
                    )

        elif model == 'AixLib': # NB NOT USED JUST FOR FURTHER DEVELOPMENT
            self.prj.used_library_calc = 'AixLib'
            self.prj.number_of_elements_calc = n_el
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

            path = self.config['folder_modelica_path']
            self.prj.export_aixlib(internal_id = None, path=path)

        else:
            raise ValueError('Unknown or Unsupported model: %s'%model)

    def convert2FMU(self, mo_name=None, mo_path=None, FMU_name=None ):

        if not mo_path and not mo_name and not FMU_name:
            for building in self.prj.buildings:
                it = [self.name,building.name, building.name+'_Models',  building.name+'_'+building.thermal_zones[0].name] # TODO NEED TO EGNERALIZE THE NAME
                mo_name = '.'.join(it)
                mo_path = os.path.join(self.config['folder_modelica_path'], self.name,'package.mo')
                FMU_name = building.name+'_FMU'
                fmu = Modelica2FMU(mo_name,mo_path,self.config['mo_lib'],FMU_name,self.config['FMU_version'],
                             self.config['FMU_type'] )
        else:
            Modelica2FMU(mo_name, mo_path, self.config['mo_lib'], FMU_name, self.config['FMU_version'],
                         self.config['FMU_type'])




    def auto_retrofit_all(self, year,info=None):
        if info == None:
            self.prj.retrofit_all_buildings(
                year_of_retrofit=year,
                type_of_retrofit="adv_retrofit",
                window_type='Alu- oder Stahlfenster, Isolierverglasung',
                material='EPS_perimeter_insulation_top_layer')
        else:
            self.prj.retrofit_all_buildings(
                year_of_retrofit = year,
                type_of_retrofit = info['type_of_retrofit'],
                window_type = info['window_type'],
                material = info['material'])

    def save_project(self, mode='json'):
        prj_path = os.path.join(self.config['folder_path'], self.name)

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
        path = os.path.join(self.config['folder_path'],self.name)
        if not os.path.exists(path):
            utilities.create_path(path)
        else:
            pass




def read_config(path):
    stream = open(path, 'r')
    dictionary = yaml.load(stream,Loader=yaml.FullLoader)
    return dictionary

residential_dict = {

    "ResidentialApartmentBlock_1"  :   {
        'method' : 'tabula_de',  # could be tabula_dk
        'usage' : 'apartment_block',
        'year_of_construction' : 1970,
        'number_of_floors' : 5,
        'height_of_floors' : 3.2,
        'net_leased_area' : 280,
        'construction_type' : 'tabula_standard'} ,

    "ResidentialApartmentBlock_2" :    {
        'method' : 'tabula_de',  # could be tabula_dk
        'usage' : 'apartment_block',
        'year_of_construction' : 1970,
        'number_of_floors' : 5,
        'height_of_floors' : 3.2,
        'net_leased_area' : 280,
        'construction_type' : 'tabula_standard'},

}



if __name__ == '__main__':
    config = read_config('config.yaml')
    prj_name = 'Residential_test'
    #instantiate the scenario project class
    PrJ = PrjScenario(config, prj_name)
    PrJ.create_buildings(residential_dict)
    PrJ.export_modelica()
    #PrJ.convert2FMU()
    #PrJ.save_project('pickle')
