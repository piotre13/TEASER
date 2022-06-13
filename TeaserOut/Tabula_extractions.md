In this file are reported the typologies of building extracted in modelica from teaser.
firstly the folder name is reported and secondly the characteristics dict.

# SingleDwellings
            dict_building = {
        'id': [0,1],
        'type': ['residential','residential'],
        'method': ['iwu','iwu'],
        'usage': ['single_family_dwelling', 'single_family_dwelling'],
        'name': ["Bui01", "Bui02",],
        'year_of_construction': [2010, 1999],
        'number_of_floors': [1,2],
        'height_of_floors': [2.75, 2.75],
        'net_leased_area': [150, 150*2],
        'with_ahu':[False,False],
        'internal_gains_mode':[1,1],
        'residential_layout':[None,None],
        'neighbour_buildings':[None,None],
        'attic':[None,None],
        'cellar':[None,None],
        'dormer':[None,None],
        'construction_type':[None,None],
        'number_of_apartments':[None, None],
    }

# ApartmentBlock_DE
        dict_building = {
        'id': [0,1,2,3,4,5,6,7],
        'type': ['residential','residential','residential','residential','residential','residential','residential','residential'],
        'method': ['tabula_de','tabula_de','tabula_de','tabula_de','tabula_de','tabula_de','tabula_de','tabula_de'],
        'usage': ['apartment_block', 'apartment_block', 'apartment_block', 'apartment_block', 'apartment_block', 'apartment_block', 'apartment_block', 'apartment_block'],
        'name': ["Bui01", "Bui02", "Bui03", "Bui04", "Bui05", "Bui06", "Bui07", "Bui08"],
        'year_of_construction': [1915,1925,1955,1965,1965,1975,1975,1975],
        'number_of_floors': [3,4,4,5,7,5,8,5],
        'height_of_floors': [2.75, 2.75, 2.75, 2.75, 2.75, 2.75, 2.75, 2.75],
        'net_leased_area': [830, 1400, 1600, 3800, 11000, 3300, 19000, 3000],
        'with_ahu':[False, False, False, False, False, False, False, False],
        'internal_gains_mode':[1,1,1,1,1,1,1,1],
        'residential_layout':[None,None,None,None,None,None,None,None],
        'neighbour_buildings':[None,None,None,None,None,None,None,None],
        'attic':[None,None,None,None,None,None,None,None],
        'cellar':[None,None,None,None,None,None,None,None],
        'dormer':[None,None,None,None,None,None,None,None],
        'construction_type':[None,None,None,None,None,None,None,None],
        'number_of_apartments':[None, None, None, None, None, None, None, None],
    }
NB ---> with these settings the building year of construction accepted are only until 1976???