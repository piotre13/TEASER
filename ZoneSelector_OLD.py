import random

import shapely.geometry as shp
from shapely.ops import transform
import osmnx.features
import pyproj
import geopandas as geopd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import fiona

fiona.supported_drivers

class TabulaReader ():
    def __init__(self, tabula_file):
        self.dfs = {}
        f = pd.ExcelFile(tabula_file)
        self.sheet_names = f.sheet_names
        self.sys_code_tmpl = '<%s.%s.%s.%s>'%(None,None,None,None)
        self.sheet_names = ['Tab.Type.Building', 'Tab.Type.System', 'Tab.System.Measure'] #filter for faster reading
        for sheet in self.sheet_names:
            #df = f.parse(sheet)
            self.dfs[sheet] = pd.read_excel(f, sheet_name=sheet, header=0)
            self.dfs[sheet] = self.dfs[sheet].iloc[9:, :]
        f.close()

    def filter_by_country(self, tabula_id):
        #we filter by country ad keep only the needed sheets
        tmp = {}
        for df in self.dfs:
            if df.startswith('Tab'):
                try:
                    tmp[df]= self.dfs[df][self.dfs[df].Code_Country == tabula_id]
                except:
                    pass
        self.dfs = tmp
        return self.dfs

    def get_building_code (self, year_construction, utilisation):
        ''' the options for utilisation are [SFH,TH,MFH,AB, MFH-AB]'''
        df = self.dfs['Tab.Type.Building']
        tmp = df[((df["Year2_Building"] >= year_construction) | (df["Year2_Building_Extension"] >= year_construction) ) & (df["Year1_Building"] <= year_construction)]
        code = [c for c in tmp.Code_BuildingType if utilisation == c.split('.')[2] ]
        return code[0]

    def get_building_systems (self, building_code, util, basic = True, **params):
        if util == 'AB' or util == 'MFH' or util == 'MFH-AB':
            build_size = 'MUH'
        else:
            build_size = 'SUH'
        sys_df = self.dfs['Tab.Type.System'][self.dfs['Tab.Type.System'].Code_BuildingSizeClass_System == build_size]

        if basic:
            sys_name = sys_df['Code_SystemType'].iloc[0]

        return sys_name
    def get_refurbishment_systems(self, sys_code):

        pass



class Zone():
    def __init__(self, study_area, tabula_file, tabula_id,output_file):

        df = geopd.read_file(study_area)
        df = df.to_crs(4326)
        try:
            polygon = shp.Polygon(df.geometry[0])
        except:
            multipolygon = shp.MultiPolygon(df.geometry[0])
            polygon = list(multipolygon.geoms)[0]

        self.study_area = polygon
        self.buildings = None
        self.zone_graph = None
        self.output_file = output_file
        Tab_reader = TabulaReader(tabula_file)
        self.tabula_df = Tab_reader.filter_by_country(tabula_id)
        self.dict_building = {
            'id': [],
            'type': [],
            'method': [],
            'usage': [],
            'name': [],
            'year_of_construction': [],
            'number_of_floors': [],
            'height_of_floors': [],
            'net_leased_area': [],
            'with_ahu': [],
            'internal_gains_mode': [],
            'residential_layout': [],
            'neighbour_buildings': [],
            'attic': [],
            'cellar': [],
            'dormer': [],
            'construction_type': [],
            'number_of_apartments': [],
        }


        pass
    def get_buildings(self):
        #convert coordinates
        #self.study_area = transform(project,self.study_area)
        self.buildings = osmnx.features.features_from_polygon(self.study_area, tags={'building':True})
        #self.zone_graph = osmnx.graph_from_polygon(self.study_area)

        print('data downloaded')

    def complete_data(self):
        self.check_data()
        #self.height()
        #self.net_leased_area()
        #self.year_of_construction()
        #self.utilisation()
        #self.archetypes()
        #self.save_gdf()
        pass

    def check_data(self):
        columns = ['geometry','name', 'nodes','building', 'building:levels', 'roof:levels', 'height','year_of_construction','amenity']
        for col in columns:
            if col not in self.buildings.columns:
                self.buildings[col]=None

        #filter useful columns
        self.buildings = self.buildings.loc[:,columns]
        #take only residentials and apartments
        #TODO using openstreetmap filtering like this could be a problem resulting in 0 buildings for the absence of the columns data
        #self.buildings = self.buildings[((self.buildings.building == 'residential')| (self.buildings.building == 'apartments'))]


    def year_of_construction(self):
        range_y = [1900,1978]
        self.buildings.year_of_construction = self.buildings.year_of_construction.apply(lambda x: round(random.randint(range_y[0],range_y[1])) if pd.isnull(x) else  x )
        self.buildings['year_of_construction'] =self.buildings['year_of_construction'].astype(int)
        pass
    def height(self):
        range_h = [5,20]
        self.buildings['h_floors'] = 3
        self.buildings.height = self.buildings.height.apply(lambda x: round(random.uniform(range_h[0],range_h[1]),2) if pd.isnull(x) else  round(float(x.split(' ')[0]),2) )
        self.buildings['floors'] =self.buildings.height/self.buildings.h_floors
        self.buildings['floors'] = self.buildings['floors'].astype(int)

    def net_leased_area(self):
        df_proj = self.buildings.to_crs('EPSG:32610')
        self.buildings['net_leased_area']=(df_proj['geometry'].area*self.buildings['floors'])-(df_proj['geometry'].area*self.buildings['floors'])*0.1
        print('stocazz')
        pass

    def utilisation(self):
        self.buildings['utilisation']= ''
        self.buildings.loc[(self.buildings['building'] == 'apartments') | (self.buildings['height'] >=9 ), 'utilisation'] = 'AB'
        self.buildings.loc[(self.buildings['height']<= 9), 'utilisation'] = 'MFH'
        pass

    def archetypes(self):
        bui_df = self.tabula_df['Tab.Type.Building'].copy()
        sys_df = self.tabula_df['Tab.Type.System'].copy().reset_index()
        self.buildings['archetype_code'] = ''
        self.buildings['sys_archetype_code']= ''
        self.buildings['sys_descr']=''
        for index, row in self.buildings.iterrows():
            util = row['utilisation']
            year = row['year_of_construction']
            code_bui = bui_df[(bui_df['Code_BuildingSizeClass']== util) & ((year<=bui_df['Year2_Building'])| (year<=bui_df['Year2_Building_Extension'])) & (year>=bui_df['Year1_Building'])]['Code_BuildingType'].values[0]
            self.buildings.at[index, 'archetype_code'] = code_bui
            self.sys_archetype(code_bui, sys_df, index)

        pass
    def sys_archetype(self, code_bui, sys_df, index):
        #todo per adesso gli ammollo il primo e vaffanculo
        possible =[24,0,26,25,28]
        sys_num = random.choice(possible)
        self.buildings.at[index,'sys_archetype_code']=sys_df.at[sys_num,'Code_SystemType']
        self.buildings.at[index,'sys_descr']= sys_df.at[sys_num,'Description_SystemType']


    def teaser_dict(self):
        di = {'AB': "apartment_block", 'MFH': "multi_family_house"}
        self.buildings= self.buildings.replace({"utilisation": di})
        self.dict_building['id']=list(range(self.buildings.shape[0]))
        self.dict_building['name']=['Bui_%s'%s for s in self.dict_building['id']]
        self.dict_building['type'] = list(self.buildings['building'])
        self.dict_building['method'] = ['tabula_de' for i in range(len(self.dict_building['id']))]
        self.dict_building['usage'] = list(self.buildings['utilisation'])
        self.dict_building['year_of_construction'] = list(self.buildings['year_of_construction'])
        self.dict_building['number_of_floors'] = list(self.buildings['floors'])
        self.dict_building['height_of_floors'] = list(self.buildings['h_floors'])
        self.dict_building['net_leased_area'] = list(self.buildings['net_leased_area'])
        self.dict_building['with_ahu']=[False for i in range(len(self.dict_building['id']))]
        self.dict_building['internal_gains_mode'] = [1 for i in range(len(self.dict_building['id']))]
        #fill with None the remaining keys
        for k in self.dict_building.keys():
            if len(self.dict_building[k]) ==0:
                self.dict_building[k]=[None for i in range(len(self.dict_building['id']))]

        return self.dict_building
    def save_gdf(self):
        #types = self.buildings.dtypes
        obj_cols = self.buildings.select_dtypes(['object']).columns.tolist()
        self.buildings[obj_cols] = self.buildings[obj_cols].astype('str')
        types = self.buildings.dtypes
        path = 'data/output/zone/'+self.output_file+'.geojson'
        self.buildings.to_file(path, driver='GeoJSON')

    def gdf2cityjson(self):
        pass


    def plot(self , kind='buildings'):
        if kind == 'buildings':
            self.buildings.plot()
            plt.show()
            plt.close()
        elif kind == 'graph':
            osmnx.plot_graph(self.zone_graph)
            plt.show()
            plt.close()

if __name__ == '__main__':

    example_geojson = 'data/limite_comunale_Frassineto.geojson'
    tabula_data = 'data/TABULA_completedataset/TABULA.xlsm'
    istat_census = 'data/R01_11_WGS84/R01_11_WGS84.shp'


    df = geopd.read_file(example_geojson)
    #polygon = shp.Polygon(df.geometry[0])
    z = Zone(example_geojson, tabula_data, 'IT','test_paper')

    z.get_buildings()
    geodf = z.buildings
    geodf = geodf.drop(columns=['nodes'])
    geodf.to_file('data/edifici_Frassinetto.shp')
    #z.complete_data()
    #bui_dict = z.teaser_dict()
    z.plot()
    #z.plot('graph')
