
"""This module is the backend for TEASER API functions.

_author_: Daniele Schiera daniele.schiera@polito.it
"""

import os

#from teaser.project import Project
#from tests.omc_backend.test_project import Project
import teaser.logic.utilities as utilities
import pandas as pd

def generate_archetype(prj, db):
    """"This function demonstrates the generation of residential and
    non-residential archetype buildings using the API function of TEASER"""

    # To use the API instantiate the Project class and rename the Project. The
    # parameter load_data=True indicates that we load `iwu` typology archetype
    # data into our Project (e.g. for Material properties and typical wall
    # constructions. This can take a few seconds, depending on the size of the
    # used data base). Be careful: Dymola does not like whitespaces in names and
    # filenames, thus we will delete them anyway in TEASER.

    # There are two different types of archetype groups: residential and
    # generate specific archetypes.

    # To generate residential archetype buildings the function
    # Project.add_residential() is used. Seven parameters are compulsory,
    # additional parameters can be set according to the used method. `method`
    # and `usage` are used to distinguish between different archetype
    # methods. The name, year_of_construction, number and height of floors
    # and net_leased_area need to be set to provide enough information for
    # archetype generation. For specific information on the parameters please
    # read the docs.
    
    # Use a dataframe db for each building with the 7 compulsory information and other free
    # i | type | method | usage | name |  year_of_construction | number_of_floors | height_of_floors | net_leased_area

    for index, row in db.iterrows():
        if row['type'] == 'residential':
            prj.add_residential(**row[2:].to_dict())
        elif row['type'] == 'nonresidential':
            prj.add_non_residential(**row[2:].to_dict())
    return prj

def export_ibpsa(prj,path=None, fmu_io=False):
    """"This function demonstrates the export to Modelica library IBPSA using
    the API function of TEASER"""

    # To make sure the export is using the desired parameters you should
    # always set model settings in the Project.
    # Project().used_library_calc specifies the used Modelica library
    # Project().number_of_elements_calc sets the models order
    # Project().merge_windows_calc specifies if thermal conduction through
    # windows is lumped into outer walls or not.
    # For more information on models we'd like to refer you to the docs. By
    # default TEASER uses a weather file provided in
    # teaser.data.input.inputdata.weatherdata. You can use your own weather
    # file by setting Project().weather_file_path. However we will use default
    # weather file.

    prj.used_library_calc = 'IBPSA'
    prj.number_of_elements_calc = 2
    prj.merge_windows_calc = False
    #prj.weather_file_path = r"D:\Projects\PycharmProjects\casestudy\uesa\resources\weather_data\USA_CA_San.Francisco.Intl.AP.724940_TMY3.mos"
    utilities.get_full_path(
        os.path.join(
            "data",
            "input",
            "inputdata",
            "weatherdata",
            "DEU_BW_Mannheim_107290_TRY2010_12_Jahr_BBSR.mos"))

    # To make sure the parameters are calculated correctly we recommend to
    # run calc_all_buildings() function

    prj.calc_all_buildings()

    # To export the ready-to-run models simply call Project.export_ibpsa().
    # First specify the IBPSA related library you want to export the models
    # for. The models are identical in each library, but IBPSA Modelica
    # library is  just a core set of models and should not be used
    # standalone. Valid values are 'AixLib' (default), 'Buildings',
    # 'BuildingSystems' and 'IDEAS'. We chose AixLib
    # You can specify the path, where the model files should be saved.
    # None means, that the default path in your home directory
    # will be used. If you only want to export one specific building, you can
    # pass over the internal_id of that building and only this model will be
    # exported. In this case we want to export all buildings to our home
    # directory, thus we are passing over None for both parameters.

    prj.export_ibpsa(
        library='AixLib',
        internal_id=None,
        path=path,
        fmu_io=fmu_io # FMU IO functionalities
    )

def export_aixlib(prj,path=None):
    """"This function demonstrates the export to Modelica library AixLib using
    the API function of TEASER"""

    #This module contains an example how to export buildings from a TEASER
    # project to ready-to-run simulation models for Modelica library AixLib. These
    # models will only simulate using Dymola, the reason for this are state
    # machines that are used in one AixLib specific AHU model.


    # To make sure the export is using the desired parameters you should
    # always set model settings in the Project.
    # Project().used_library_calc specifies the used Modelica library
    # Project().number_of_elements_calc sets the models order
    # For more information on models we'd like to refer you to the docs. By
    # default TEASER uses a weather file provided in
    # teaser.data.input.inputdata.weatherdata. You can use your own weather
    # file by setting Project().weather_file_path. However we will use default
    # weather file.
    # Be careful: Dymola does not like whitespaces in names and filenames,
    # thus we will delete them anyway in TEASER.

    prj.used_library_calc = 'AixLib'
    prj.number_of_elements_calc = 2
    prj.weather_file_path = utilities.get_full_path(
        os.path.join(
            "data",
            "input",
            "inputdata",
            "weatherdata",
            "USA_CA_San.Francisco.Intl.AP.724940_TMY3.mos"))
            #"DEU_BW_Mannheim_107290_TRY2010_12_Jahr_BBSR.mos"))

    # To make sure the parameters are calculated correctly we recommend to
    # run calc_all_buildings() function

    prj.calc_all_buildings()

    # To export the ready-to-run models simply call Project.export_aixlib().
    # You can specify the path, where the model files should be saved.
    # None means, that the default path in your home directory
    # will be used. If you only want to export one specific building, you can
    # pass over the internal_id of that building and only this model will be
    # exported. In this case we want to export all buildings to our home
    # directory, thus we are passing over None for both parameters.

    prj.export_aixlib(
        internal_id=None,
        path=path)


def save_project(prj):
    """"This function demonstrates different saving options of TEASER"""

    # In e1_generate_archetype we created a Project with three archetype
    # buildings to get this Project we rerun this example

    #prj = e1.example_generate_archetype()

    # First option is to use TEASERs own XML format to save all relevant
    # data into a more or less human readable format. The corresponding
    # function is called Project().save_project() you can specify a file name
    #  and a save path. If both are non (as in this case) it will use the
    # projects name and default path in your home folder.

    prj.save_project(file_name=None, path=None)

    # Second option is to use pickle from Python Standard Library ,
    # which will save the whole Python classes and all attributes into a
    # binary file. There is no specific API function for this, but you can
    # simply create an empty file with open() and then use pickle.dump().
    # Make sure you specify your path correctly. In this case we want to use
    # the default path of TEASERs output.

    import pickle

    pickle_file = os.path.join(
        utilities.get_default_path(),
        'teaser_pickle.p')

    pickle.dump(prj, open(pickle_file, "wb"))

def load_project(filename):
    """"This function demonstrates different loading options of TEASER"""

    # In example e4_save we saved two TEASER projects using *.teaserXML and
    # Python package pickle. This example shows how to import these
    # information into your python environment again.

    # To load data from *.teaserXML we can use a simple API function. So
    # first we need to instantiate our API (similar to example
    # e1_generate_archetype). The XML file is called
    # `ArchetypeExample.teaserXML` and saved in the default path. You need to
    #  run e4 first before you can load this example file.

    from teaser.project import Project

    prj = Project()

    load_xml = os.path.join(
        utilities.get_default_path(),
        'ArchetypeExample.teaserXML')

    prj.load_project(
        path=load_xml)
    prj = Project()
    prj.load_project(utilities.get_full_path(
        "examples/examplefiles/new.teaserXML"))
    prj.save_project(file_name="new", path=None)

    # To reload data from a pickle file, we do not need to instantiate an
    # API, as pickle will automatically instantiate all classes as they have
    # been saved. The saved file from example e4 is called ´teaser_pickle.p´

    import pickle

    load_pickle = os.path.join(
        utilities.get_default_path(),
        'teaser_pickle.p')

    pickle_prj = pickle.load(open(load_pickle, "rb"))
    print(pickle_prj)
    # The last option to import data into TEASER is using a CityGML file. The
    # import of CityGML underlies some limitations e.g. concerning data
    # given in the file and the way the buildings are modeled.

    prj_gml = Project()

    load_gml = utilities.get_full_path(os.path.join(
        'examples',
        'examplefiles',
        'CityGMLSample.gml'))

    prj_gml.load_citygml(path=load_gml)

    # After you imported your teaser project one or another way into you
    # python environment you can access variables and functions.
    
def eretrofit_building(prj):
    """"This function demonstrates retrofit options of TEASER API"""

    # To apply simplified retrofit for all buildings in the project we can
    # use Project.retrofit_all_buildings() function. This will retrofit all
    # building in the project in following manner:
    # 1. Replace all window with a new window (default is EnEv window with
    # U-Value of XYZ
    # 2. Add an additional insulation layer to all outer walls (including,
    # roof and ground floor). Set the thickness that it corresponds to the
    # retrofit standard od the year of retrofit.
    # The year of retrofit has to be specified. In addition, we can set
    # the used window_type and the type of insulation material used.
    # As we have both `iwu`/`bmvbs` and `tabuly` typology in our project we need
    # to pass all keywords to the function year_of_retrofit, window_type,
    # material for `iwu`/`bmvbs` and type_of_retrofit for `tabula`.

    prj.retrofit_all_buildings(
        year_of_retrofit=2015,
        type_of_retrofit="adv_retrofit",
        window_type='Alu- oder Stahlfenster, Isolierverglasung',
        material='EPS_perimeter_insulation_top_layer')


if __name__ == '__main__':
    # Use a dataframe db for each building with the 7 compulsory information and other free
    # id | type | method | usage | name |  year_of_construction | number_of_floors | height_of_floors | net_leased_area
    # dict_building = {
    #     'id': [0,1],
    #     'type': ['residential','nonresidential'],
    #     'method': ['iwu','bmvbs'],
    #     'usage': ['single_family_dwelling','office'],
    #     'name': ["ResidentialBuilding",'OfficeBuilding'],
    #     'year_of_construction': [1988,1988],
    #     'number_of_floors': [2,4],
    #     'height_of_floors': [3.2,3.5],
    #     'net_leased_area': [200,4500]
    # }
    # #
    dict_building = {
        'id': [0],
        'type': ['residential'],
        'method': ['iwu'],
        'usage': ['single_family_dwelling'],
        'name': ["ResidentialBuilding"],
        'year_of_construction': [2010],
        'number_of_floors': [1],
        'height_of_floors': [2.75],
        'net_leased_area': [150]
    }
    db = pd.DataFrame.from_dict(dict_building)
    prj = generate_archetype('Building', db)
    om_models_dir = r"D:\Projects\PycharmProjects\casestudy\models\openmodelica"
    export_ibpsa(prj,om_models_dir,fmu_io=True)
    #export_aixlib(prj, om_models_dir)