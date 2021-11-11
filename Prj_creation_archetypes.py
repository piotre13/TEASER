from teaser.project import Project
import teaser.logic.utilities as utilities
import yaml
import os
import pickle


class PrjScenario:
    def __init__(self, config, prj_name):
        self.config = config
        self.name = prj_name
        self.prj = Project() #TODO CHECK IF POSSIBLE TO USE SUPER INIT
        self.prj.name = self.name
        self.prj.weather_file_path = config['weather_path']
        #print(self.config)
        self.create_prj_folder() #creating the folder if first time

    def create_residentials(self,info=None):
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
        if info:
            print('buildings info specified by user')
            #TODO ADD CREATION FROM SPECIFIED DICT OF INFO
        else:
            print('using method example buildings: 5 buildings')
            for i in range(5):  # ne genero 5
                self.prj.add_residential(
                    method='tabula_de', # could be tabula_dk
                    usage='apartment_block',
                    name="ResidentialApartmentBlock_%s" % i,
                    year_of_construction=1970,
                    number_of_floors=5,
                    height_of_floors=3.2,
                    net_leased_area=280,
                    construction_type='tabula_standard'
                )

    def create_non_residentials(self, info= None):
        #todo create non residential for variety
        pass
    def create_from_shp(self, shp_file):
        #TODO create a scenario from shapefile
        pass
    def export_modelica_all(self, weather=None, n_el=2, model='AixLib',library= 'AixLib'):
        '''library for IBPSA export has to be 'AixLib',
            'Buildings', 'BuildingSystems' or 'IDEAS' '''
        #TODO GENERALISE THE FOLDER WHERE TO EXPORT the modelica models create self variables
        if model == 'AixLib':
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
                self.prj.calc_all_buildings()
            except:
                raise ValueError('Parameters for modelica model are not ok!')

            path = os.path.join(self.config['folder_modelica_path'],'aixlib')
            self.prj.export_aixlib(internal_id = None, path=path)


        elif model == 'IBPSA':
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
                self.prj.calc_all_buildings()
            except:
                raise ValueError('Parameters for modelica model are not ok!')

            path = os.path.join(self.config['folder_modelica_path'],'ibpsa')
            self.prj.export_ibpsa(
                    library= library,
                    internal_id=None,
                    path=path)

        else:
            raise ValueError('Unknown or Unsupported model: %s'%model)

    def export_modelica_single(self, building_id, n_el=2, model='AixLib'):
        pass
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

    def save_project(self,mode='json'):
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
        modelica_path = self.config['folder_modelica_path']
        if not os.path.exists(modelica_path):
            utilities.create_path(modelica_path)
        else:
            pass



def read_config(path):
    stream = open(path, 'r')
    dictionary = yaml.load(stream,Loader=yaml.FullLoader)
    return dictionary





if __name__ == '__main__':
    config = read_config('config.yaml')
    Prj = PrjScenario(config,'PRJ_test')
    Prj.create_residentials() # specify an info file with infos and number of buildings to be created or leave it as it is
    Prj.save_project(mode='pickle') #no mode will save in json teaser format
    Prj.save_project() #no mode will save in json teaser forma
    Prj.export_modelica_all(model='IBPSA') # can specify AixLib or IPBSA, number of calc components and different specific weather path
    print(Prj.prj)
