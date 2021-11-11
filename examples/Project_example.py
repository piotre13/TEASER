from teaser.project import Project

# this function is used to create a project by generating archetypes try to use one method at a time do not mix them
#

def example_generate_archetypes():

        prj = Project(load_data= False) # instantiate class project # if only using tabula archteypes set load_data to False
        prj.name = 'Example_prj'


        #this actually creates a building
        for i in range(5): # ne genero 5
                prj.add_residential(
                        method='tabula_de',
                        usage='apartment_block',
                        name="ResidentialApartmentBlock_%s"%i,
                        year_of_construction=1970,
                        number_of_floors=5,
                        height_of_floors=3.2,
                        net_leased_area=280,
                        construction_type='tabula_standard'
                        )
        return prj

if __name__ == '__main__':

        prj = example_generate_archetypes()
        print(prj)