from Project_example import example_generate_archetypes as e1
import teaser.logic.utilities as utilities
import os

def example_save():
    """"This function demonstrates different saving options of TEASER"""
    prj = e1()

    # First option is to use TEASERs own XML format to save all relevant
    # data into a more or less human readable format. The corresponding
    # function is called Project().save_project() you can specify a file name
    #  and a save path. If both are non (as in this case) it will use the
    # projects name and default path in your home folder.

    prj.save_project(file_name= 'Example_prj', path='/Users/pietrorandomazzarino/Documents/DOTTORATO/CODE/TEASER/TeaserOut')

    # Second option is to use pickle from Python Standard Library ,
    # which will save the whole Python classes and all attributes into a
    # binary file. There is no specific API function for this, but you can
    # simply create an empty file with open() and then use pickle.dump().
    # Make sure you specify your path correctly. In this case we want to use
    # the default path of TEASERs output.

    import pickle

    #pickle_file = os.path.join(
    #    utilities.get_default_path(),
    #    'teaser_pickle.p')
    pickle_file = '/TeaserOut/example_prj/example_prj.p'
    pickle.dump(prj, open(pickle_file, "wb"))



from teaser.project import Project
def example_load():
    """"This function demonstrates different loading options of TEASER"""


    #first example of loading the json file (don't know where the xml option is...
    prj = Project()
    load_path = '/TeaserOut/example_prj/Example_prj.json'
    prj.load_project(
        path=load_path)
    print(prj)

    # To reload data from a pickle file, we do not need to instantiate an
    # API, as pickle will automatically instantiate all classes as they have
    # been saved. The saved file from example e4 is called ´teaser_pickle.p´
    import pickle
    load_pickle = '/Users/pietrorandomazzarino/Documents/DOTTORATO/CODE/TEASER/TeaserOut/example_prj.p'

    pickle_prj = pickle.load(open(load_pickle, "rb"))
    print(pickle_prj)


    #citygml does not work or exist anymore
    # The last option to import data into TEASER is using a CityGML file. The
    # import of CityGML underlies some limitations e.g. concerning data
    # given in the file and the way the buildings are modeled.

    # prj_gml = Project()
    #
    # load_gml = utilities.get_full_path(os.path.join(
    #     'examples',
    #     'examplefiles',
    #     'CityGMLSample.gml'))
    #
    # prj_gml.load_citygml(path=load_gml)
    #
    # print(prj_gml)

    # After you imported your teaser project one or another way into you
    # python environment you can access variables and functions.

if __name__ == '__main__':
   # example_save()
    example_load()
