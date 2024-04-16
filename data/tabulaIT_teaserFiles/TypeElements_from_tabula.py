import json
import pandas as pd


template_element ={
    "OuterWall_[0, 1859]_tabula_standard_1_SFH": {
        "building_age_group": [
            0,
            1859
        ],
        "construction_type": "tabula_standard_1_SFH",
        "inner_radiation": 5.0,
        "inner_convection": 2.7,
        "outer_radiation": 5.0,
        "outer_convection": 20.0,
        "layer": {
            "0": {
                "thickness": 0.16,
                "material": {
                    "name": "fibrous_loam_1200",
                    "material_id": "266228a4-3a43-11e7-acde-2cd444b2e704"
                }
            }
        }
    },
}


class TabulaReader ():
    def __init__(self, tabula_file):
        self.dfs = {}
        f = pd.ExcelFile(tabula_file)
        self.sheet_names = f.sheet_names
        self.sys_code_tmpl = '<%s.%s.%s.%s>'%(None,None,None,None)
        self.sheet_names = ['Tab.Type.Building','Tab.Const.ElementType', 'Tab.Building.Constr', 'Tab.Building', 'Tab.Building.Measure'] #filter for faster reading
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


class TeaserInputsCreator():
    def __init__(self, tabula_dfs, files):
        self.dfs = tabula_dfs
        self.files = {}
        self.read_filesJson(files)
        #self.type_el_name_templ =
        self.type_elements_templ = {
        "building_age_group": [],
        "construction_type": "",
        "inner_radiation": None,
        "inner_convection": None,
        "outer_radiation": None,
        "outer_convection": None,
        "layer": {
            "0": {
                "thickness": None,
                "material": {
                    "name": "",
                    "material_id": ""
                }
            },
        }
        }
    def read_filesJson(self, files):
        for key, path in files.items():
            with open(path) as f:
                try:
                    self.files[key]=json.load(f)
                except:
                    pass
    def typeElements_empty(self):
        num_type = len(self.files['type_DE'])
        num_tab = self.dfs['Tab.Building'].shape
        print('yo')




# file_template = '../../teaser_fork_final/data/input/inputdata/MaterialTemplates.json'
# with open(file_template) as f :
#     data = json.load(f)
# print(len(data.keys()))
# print(data)elements


if __name__ == '__main__':
    #READ tabula
    tabula_file = '/home/pietrorm/Documents/CODE/TEASER/data/TABULA_completedataset/TABULA.xlsm'
    reader = TabulaReader(tabula_file)
    dfs = reader.filter_by_country('DE')





    output_files = {'type_DE': '/home/pietrorm/Documents/CODE/TEASER/teaser_fork_final/data/input/inputdata/TypeElements_TABULA_DE.json',
                    'type_IT': '/home/pietrorm/Documents/CODE/TEASER/teaser_fork_final/data/input/inputdata/TypeElements_TABULA_IT.json',
                    'material_template': '/home/pietrorm/Documents/CODE/TEASER/teaser_fork_final/data/input/inputdata/MaterialTemplates.json'}

    creator = TeaserInputsCreator(dfs,output_files)
    creator.typeElements_empty()
    print('ciao')