from Prj_creation_archetypes import PrjScenario as Prj
from utils import read_config
import geopandas as gpd
import pprint

class Cea2Teaser():
    def __init__(self, shp_path):
        self.path = shp_path
        self.zone = self.read_shp()
        self.fields = ['id','type', 'method', 'usage', 'name', 'year_of_construction','number_of_floors','height_of_floors','net_leased_area','with_ahu','internal_gains_mode',
                     'residential_layout', 'neighbour_buildings', 'attic','cellar','dormer','construction_type','number_of_apartments']
        self.teaser_dict= None
    def read_shp(self):
        zone = gpd.read_file(self.path)
        #lower all the column names
        zone.columns = map(str.lower, zone.columns)
        return zone
    def run_conversion(self):
        for field in self.fields:
            if field not in list(self.zone.columns):
                if field == 'id':
                    self.get_id()
                elif field == 'type':
                    self.get_type()
                elif field == 'method':
                    self.get_method()
                elif field == 'usage':
                    self.get_usage()
                elif field == 'name':
                    self.get_name()
                elif field == 'year_of_construction':
                    self.get_year_of_construction()
                elif field == 'number_of_floors':
                    self.get_number_of_floors()
                    pass
                elif field == 'height_of_floors':
                    self.get_height_of_floors()
                    pass
                elif field == 'net_leased_area':
                    self.calc_net_leased_area()
                elif field == 'with_ahu':
                    self.get_with_ahu()
                elif field == 'internal_gains_mode':
                    self.get_internal_gains_mode()
                elif field == 'residential_layout':
                    self.get_residential_layout()
                elif field == 'neighbour_buildings':
                    self.get_neighbour_buildings()
                elif field =='attic':
                    self.get_attic()
                elif field == 'cellar':
                    self.get_cellar()
                elif field == 'dormer':
                    self.get_dormer()
                elif field == 'construction_type':
                    self.get_construction_type()
                elif field =='number_of_apartments':
                    self.get_number_of_apartments()
        self.create_dict()
        return self.teaser_dict

    def create_dict(self):
        #keep ony the tease fields
        df = self.zone[self.fields]
        self.teaser_dict =  df.to_dict('list')
    def calc_net_leased_area(self):
        #todo togliere una percentuale
        self.zone['net_leased_area'] = self.zone['geometry'].area * (self.zone['floors_ag']+self.zone['floors_bg'])

    def get_id(self):
        self.zone["id"] = self.zone.index + 1

    def get_type(self):
        self.zone['type'] ='residential'

    def get_method(self):
        self.zone['method'] = 'tabula_de'

    def get_name(self):
        self.zone['name'] = ['Bui_'+str(i) for i in range(len(self.zone.index))]

    def get_usage(self):
        self.zone['usage'] = 'apartment_block'

    def get_year_of_construction(self):
        self.zone['year_of_construction'] = 1965

    def get_number_of_floors(self):
        self.zone['number_of_floors'] = self.zone['floors_ag'] + self.zone['floors_bg'] # this valid with cea

    def get_height_of_floors(self):
        hgt_mean = self.zone['height_ag']/self.zone['floors_ag']
        self.zone['height_of_floors'] = hgt_mean

    def get_with_ahu(self):
        self.zone['with_ahu'] = False

    def get_internal_gains_mode(self):
        self.zone['internal_gains_mode'] = 1

    def get_residential_layout(self):
        self.zone['residential_layout'] = None

    def get_neighbour_buildings(self):
        n_neigh = []
        for index, row in self.zone.iterrows():
            neighbors = self.zone[self.zone.geometry.touches(row['geometry'])].name.tolist()
            n_neigh.append(len(neighbors))
        self.zone['neighbour_buildings'] = n_neigh

    def get_attic(self):
        self.zone['attic'] = 0

    def get_cellar(self):
        self.zone['cellar'] = 0

    def get_dormer(self):
        self.zone['dormer'] = None

    def get_construction_type(self):
        self.zone['construction_type'] = None

    def get_number_of_apartments(self):
        self.zone['number_of_apartments'] = None


if __name__ == '__main__':
    zone_path = "/home/pietrorm/Documents/CODE/TEASER/data/baseline/inputs/building-geometry/zone.shp"
    sorroundings_path = '/home/pietrorm/Documents/CODE/TEASER/data/baseline/inputs/building-geometry/surroundings.shp'
    C = Cea2Teaser(zone_path)
    teaser_dict = C.run_conversion()
    pprint.pprint (teaser_dict)
    config = read_config('config.yaml')
    prj_name = 'test_MES_CeaSingapore'
    project = Prj(config, prj_name)
    project.create_buildings_from_input(teaser_dict)
    project.export_modelica(weather=None, n_el=None, model=None, library=None, single_bui=None, template=None,
                            fmu_io=None)
