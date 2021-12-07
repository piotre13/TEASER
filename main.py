from Prj_creation_archetypes import PrjScenario as Prj
from teaser.logic.buildingobjects.calculation.one_element import OneElement as One
from teaser.logic.buildingobjects.thermalzone import ThermalZone
import yaml


def read_config(path):
    stream = open(path, 'r')
    dictionary = yaml.load(stream,Loader=yaml.FullLoader)
    return dictionary


if __name__ == '__main__':
    config = read_config('config.yaml')

    #Creating a scenario and saving****************
    Scenario = Prj(config,'PRJ_test')
    Scenario.create_residentials() # specify an info file with infos and number of buildings to be created or leave it as it is

    Scenario.save_project(mode='pickle') #no mode will save in json teaser format
    Scenario.export_modelica_all(model='IBPSA')
    print(Scenario.prj)
    #***********************************************

    #Loading a scenario*****************************
    #path_json = '/Users/pietrorandomazzarino/Documents/DOTTORATO/CODE/TEASER/TeaserOut/PRJ_test/PRJ_test.json'
    #path_pickle = '/Users/pietrorandomazzarino/Documents/DOTTORATO/CODE/TEASER/TeaserOut/PRJ_test/PRJ_test.p'
    #Scenario = Prj(config, 'PRJ_test')
    #Scenario.load_project(path_json)
    #Scenario.load_project(path_pickle)
    #print(Scenario.prj)
    #***********************************************

    #exporting modelica models *********************
    #Scenario = Prj(config,'PRJ_test')
    #Scenario.export_modelica_all(weather=None, n_el=2, model='AixLib')
    # is possible to specify IBPSA or AixLib the number of element calc and the weather file
    #***********************************************

    #path_json = '/Users/pietrorandomazzarino/Documents/DOTTORATO/CODE/TEASER/TeaserOut/TEA_scenarios/PRJ_test/PRJ_test.json'
    #Scenario = Prj(config, 'PRJ_test2')
    #Scenario.load_project(path_json)
    #prj = Scenario.prj
    #Scenario.export_modelica_all(model='IBPSA',library= 'Buildings')