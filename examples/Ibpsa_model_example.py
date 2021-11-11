from Project_example import example_generate_archetypes as e1
import teaser.logic.utilities as utilities
import os



def example_export_ibpsa():
    prj = e1()
    prj.used_library_calc = 'IBPSA'
    prj.number_of_elements_calc = 4
    prj.merge_windows_calc = False
    prj.weather_file_path = utilities.get_full_path(
        os.path.join(
            "data",
            "input",
            "inputdata",
            "weatherdata",
            "DEU_BW_Mannheim_107290_TRY2010_12_Jahr_BBSR.mos"))
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
        path='/TeaserOut/example_prj_ibpsa')


if __name__ == '__main__':
    example_export_ibpsa()