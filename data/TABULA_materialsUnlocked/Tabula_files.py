import json
import pandas as pd
from itertools import islice
import copy
def read_json(file_path):
	with open(file_path,'r') as fp:
		data = json.load(fp)
	return data

def read_xlsx(file_path, sheet_name=0, skiprows=None):
	data = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=skiprows)
	return data

def add_material(mat_id):
	pass


def fill_tabula_file(input, out_file):
	list_unique_materials = []
	materials_dict = {}
	out_file["version"] = "0.7"
	base_dict = {"building_age_group":[],
				 "construction_type":"",
				 "inner_radiation":5.0,
				 "inner_convection":1.7,
				 "outer_radiation":5.0,
				"outer_convection": 20.0,
				 "layer":{}}
	for index, row in islice(input.iterrows(), 1, None):
		if '-' in row['Unnamed: 1']:
			a = row['Unnamed: 1'].split('-')[0]
			b = row['Unnamed: 1'].split('-')[1]
			period = f'[{a}, {b}]'
		else:
			a=row['Unnamed: 1'][-4:]
			period = f'[0, {a}]'

		typology = row['Unnamed: 0'][:-3]

		#**************** WALLS *****************************
		const_id = 'OuterWall_'+period+'_tabula_standard_1_'+typology
		base_dict['building_age_group']=[int(period.split(',')[0][1:]),int(period.split(',')[1][:-1])]
		base_dict['construction_type'] = 'tabula_standard_1_'+typology
		base_dict['layer'], list_unique_materials, materials_dict = get_layers(row['Unnamed: 7'], list_unique_materials, materials_dict)
		#Out_wall1 = {const_id : base_dict}
		out_file [const_id] = copy.deepcopy(base_dict)
		#todo add retrofit value and ceiling, floor and roof get layers method should always work
		#todo in caso il codice sia NaN bisogna sospendere getlayer e sospendere la creazione della entry nell out file

		# todo must be added the retrofit values
		if not pd.isna(row['Unnamed: 9']) :
			const_id = 'OuterWall_'+period+'_tabula_retrofit_1_'+typology
			base_dict['building_age_group']=[int(period.split(',')[0][1:]),int(period.split(',')[1][:-1])]
			base_dict['construction_type'] = 'tabula_standard_1_' + typology
			base_dict['layer'], list_unique_materials, materials_dict = get_layers(row['Unnamed: 9'],
																				   list_unique_materials,
																				   materials_dict)
			# Out_wall1 = {const_id : base_dict}
			out_file[const_id] = copy.deepcopy(base_dict)
		if not pd.isna(row['Unnamed: 11']) :
			const_id = 'OuterWall_'+period+'_tabula_retrofit_2_'+typology
			base_dict['building_age_group']=[int(period.split(',')[0][1:]),int(period.split(',')[1][:-1])]
			base_dict['construction_type'] = 'tabula_standard_1_' + typology
			base_dict['layer'], list_unique_materials, materials_dict = get_layers(row['Unnamed: 11'],
																				   list_unique_materials,
																				   materials_dict)
			# Out_wall1 = {const_id : base_dict}
			out_file[const_id] = copy.deepcopy(base_dict)


		#**************** CEILINGS *****************************
		if not pd.isna(row['Unnamed: 5']) :
			const_id = 'Ceiling_'+period+'_tabula_standard_1_'+typology
			base_dict['building_age_group']=[int(period.split(',')[0][1:]),int(period.split(',')[1][:-1])]
			base_dict['construction_type'] = 'tabula_standard_1_' + typology
			base_dict['layer'], list_unique_materials, materials_dict = get_layers(row['Unnamed: 5'], list_unique_materials,
																				   materials_dict)
			# Out_wall1 = {const_id : base_dict}
			out_file [const_id] = copy.deepcopy(base_dict)

		#**************** ROOFS *****************************
		const_id = 'Rooftop_' + period + '_tabula_standard_1_'+typology
		base_dict['building_age_group']=[int(period.split(',')[0][1:]),int(period.split(',')[1][:-1])]
		base_dict['construction_type'] = 'tabula_standard_1_' + typology
		base_dict['layer'], list_unique_materials, materials_dict = get_layers(row['Unnamed: 3'], list_unique_materials,
																			   materials_dict)
		out_file [const_id] = copy.deepcopy(base_dict)

		#**************** FLOORS *****************************
		const_id = 'GroundFloor_'+period+'_tabula_standard_1_'+typology
		base_dict['building_age_group']=[int(period.split(',')[0][1:]),int(period.split(',')[1][:-1])]
		base_dict['construction_type'] = 'tabula_standard_1_' + typology
		base_dict['layer'], list_unique_materials, materials_dict = get_layers(row['Unnamed: 13'], list_unique_materials,
																			   materials_dict)
		out_file [const_id] = copy.deepcopy(base_dict)

		if not pd.isna(row['Unnamed: 15']) :
			const_id = 'GroundFloor_'+period+'_tabula_retrofit_1_'+typology
			base_dict['building_age_group']=[int(period.split(',')[0][1:]),int(period.split(',')[1][:-1])]
			base_dict['construction_type'] = 'tabula_standard_1_' + typology
			base_dict['layer'], list_unique_materials, materials_dict = get_layers(row['Unnamed: 15'],
																				   list_unique_materials,
																				   materials_dict)
			# Out_wall1 = {const_id : base_dict}
			out_file[const_id] = copy.deepcopy(base_dict)



	#writing files
	with open('tabula_it_nowin.json', 'w', encoding='utf-8') as f:
		json.dump(out_file, f, ensure_ascii=False, indent=4)

	# with open('/home/pietrorm/Documents/CODE/TEASER/teaser_fork_final/data/input/inputdata/MaterialTemplates.json', 'r') as f:
	# 	mat_data = json.load(f)
	# 	mat_data.update(materials_dict)
	# with open('/home/pietrorm/Documents/CODE/TEASER/teaser_fork_final/data/input/inputdata/MaterialTemplates.json','w') as f:
	# 	json.dump(mat_data, f)
	print('end of loop')


def get_layers(code, material_list, mat_dict):
	layer_dict = {}

	file_name = 'Tabula_stratigrafie/'+code+'.xlsx'
	data = read_xlsx(file_name, sheet_name='Caratteristiche componente', skiprows=3)
	col=[0,1]
	for i in range(21): col.append(9+i)
	data = data.drop(data.columns[col], axis=1)
	data = data.dropna(how = 'all')
	j =0
	for index, row in data.iterrows():
		material_dict = {}
		tmpl = row['Unnamed: 2']
		if not pd.isna(row['Unnamed: 2']) :
			print(tmpl)
			if row['Unnamed: 2'] not in material_list:
				unique_id = 'mat_ccc_'+'%s'%len(material_list)
				mat_dict[unique_id]=  material_dict
				material_list.append(row['Unnamed: 2'])
				material_dict['name']= row['Unnamed: 2']
				material_dict['density']= row['r']
				material_dict['thermal_conduc']= row['l']
				material_dict['heat_capac']= row['c']/1000 #in Kj/KgC
				material_dict['thickness_default']= row['s']
				material_dict['thickness_list']= []
			else:
				for key, val in mat_dict.items():
					if val['name'] == row['Unnamed: 2']:
						unique_id = key
						if row['s'] != mat_dict[unique_id]['thickness_default'] and row['s'] not in mat_dict[unique_id]['thickness_list']:
							mat_dict[unique_id]['thickness_list'].append(row['s'])


			layer_dict[str(j)]={}
			layer_dict[str(j)]['thickness'] = row['s']
			layer_dict[str(j)]['material']={}
			layer_dict[str(j)]['material']['name'] = row['Unnamed: 2']
			layer_dict[str(j)]['material']['material_id'] = unique_id
			j+=1



	# 		material_dict["name"] = data.loc
	# 		material_dict["density"] =
	# 		material_dict["thermal_conduc"] =
	# 		material_dict["heat_capac"] =
	# 		material_dict["thickness_default"] =
	# 		material_dict["thickness_list"]= []
	# 		material_dict["solar_absorp"]= 0.5


	#todo open the specific code file
	return layer_dict, material_list, mat_dict

if __name__ == '__main__':
	materials_file = '../../teaser_fork_final/data/input/inputdata/MaterialTemplates.json'
	template_tabula = '/home/pietrorm/Documents/CODE/TEASER/teaser_fork_final/data/input/inputdata/TypeElements_TABULA_DE.json'
	tabula_IT = '/home/pietrorm/Documents/CODE/TEASER/teaser_fork_final/data/input/inputdata/TypeElements_TABULA_IT.json'

	constr = '/home/pietrorm/Documents/CODE/TEASER/data/TABULA_materialsUnlocked/TABULA_Codici_costruzioni.xlsx'

	data1 = read_json(materials_file)
	data2 = read_json(template_tabula)
	data3 = read_json(tabula_IT)

	data4 = read_xlsx(constr)

	fill_tabula_file(data4, data3)

	print('yo')