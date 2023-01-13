# PIPELINE WORKFLOW
1. TEASER ---> main.py using Project_creation_archetypes.py (it create a teaser and a modelica project for the given buildings)
2. FMU creation ---> FMUs/create_fmu.py (convert a single building .mo file into FMU)
3. SIMULATE FMU ---> FMUs/FMU_simul_test.py (simulate an FMU)


# TEASER - FMU pipeline
## annotations pre simulation:
1. nel nuovo template bisognerebbe ricopiare una a una le annotazioni dei componenti dal pacchetto così che quando si carica su OMEdit non vcenga brutto e tutto sbalòlato
2. ridefinire i template e i modelli modelica in modo che input e output e parametri 
   1. rifare il modello in modelica per bene
   2. rifare il package per heater cooler per bene
   3. rifare template per TEASER
3. siano ordinati e ci sia uno standard fisso per il passaggio datoi tra un modello e i suoi sottomodelli
4. **PROBLEMA** create_fmu() ---> Modelica2Fmu() salva le fmu nella cartella in cui si trova, difficile da integrare in PrjArchetypes(class) 
5. estrarre la possibilità di simulare la fmu con gli input da file come quando simulo in modelica per test STAND ALONE
   1. **Risolto**: nel template per teaser ho cambiato da **ln 24-35 .Input in .File**
   2. in particular line 26 .File inplace of .Input_HDirNor_HDifHor
6. 
## annotations FMU simulation:
1. model_description sembra non contenere gli input gia separati per creare un record, invece gli output si
2. trovare un modo per facilmente retrivare gli inputs
# Folder Structure
   

# DESCRIPTION of input for teaser building dict
                 method : str
            Used archetype method, currently only 'iwu' or 'urbanrenet' are
            supported, 'tabula_de' to follow soon
        usage : str
            Main usage of the obtained building, currently only
            'single_family_dwelling' is supported for iwu and 'est1a', 'est1b',
            'est2', 'est3', 'est4a', 'est4b', 'est5' 'est6', 'est7', 'est8a',
            'est8b' for urbanrenet.
        name : str
            Individual name
        year_of_construction : int
            Year of first construction
        height_of_floors : float [m]
            Average height of the buildings' floors
        number_of_floors : int
            Number of building's floors above ground
        net_leased_area : float [m2]
            Total net leased area of building. This is area is NOT the
            footprint
            of a building
        with_ahu : Boolean
            If set to True, an empty instance of BuildingAHU is instantiated
            and
            assigned to attribute central_ahu. This instance holds information
            for central Air Handling units. Default is False.
      internal_gains_mode: int [1, 2, 3]
        mode for the internal gains calculation done in AixLib:
        1: Temperature and activity degree dependent heat flux calculation for persons. The
           calculation is based on  SIA 2024 (default)
        2: Temperature and activity degree independent heat flux calculation for persons, the max.
           heatflowrate is prescribed by the parameter
           fixed_heat_flow_rate_persons.
        3: Temperature and activity degree dependent calculation with
           consideration of moisture and co2. The moisture calculation is
           based on SIA 2024 (2015) and regards persons and non-persons, the co2 calculation is based on
           Engineering ToolBox (2004) and regards only persons.
        residential_layout : int
            Structure of floor plan (default = 0) CAUTION only used for iwu
                0: compact
                1: elongated/complex
        neighbour_buildings : int
            Number of neighbour buildings. CAUTION: this will not change
            the orientation of the buildings wall, but just the overall
            exterior wall and window area(!) (default = 0)
                0: no neighbour
                1: one neighbour
                2: two neighbours
        attic : int
            Design of the attic. CAUTION: this will not change the orientation
            or tilt of the roof instances, but just adapt the roof area(!) (
            default = 0) CAUTION only used for iwu
                0: flat roof
                1: non heated attic
                2: partly heated attic
                3: heated attic
        cellar : int
            Design of the of cellar CAUTION: this will not change the
            orientation, tilt of GroundFloor instances, nor the number or area
            of ThermalZones, but will change GroundFloor area(!) (default = 0)
            CAUTION only used for iwu
                0: no cellar
                1: non heated cellar
                2: partly heated cellar
                3: heated cellar
        dormer : str
            Is a dormer attached to the roof? CAUTION: this will not
            change roof or window orientation or tilt, but just adapt the roof
            area(!) (default = 0) CAUTION only used for iwu
                0: no dormer
                1: dormer
        construction_type : str
            Construction type of used wall constructions default is "heavy")
                heavy: heavy construction
                light: light construction
        number_of_apartments : int
            number of apartments inside Building (default = 1). CAUTION only
            used for urbanrenet

# Output folder structure (Modelica project model)
      project folder # name of the project
      +-- Building1 folder #name of the building
          +-- Building1 models folder # name of the building + '_Models'
               +-- Building1 modelica model # .mo file name of the building + '_TypeArchetype' e.g. Bui1_SingleDwelling
               +-- internal gains file #.txt
               +-- packages files as in the others
          +-- package order # package.order file with the order of modelica packages
          +-- package # actuale .mo file for the building (seems not loadble)
            
      +-- Building2 folder #name of the building
          +-- ...
      +-- ...
      +-- weather file #.mos file
      +-- package order # package.order file with the order of modelica packages
      +-- package # actuale .mo file for the entire project (load this on OM)


# TEASER
## problems:


# CREATE fmu
## problems:
1. export the solver (using flag for cvode) Are we really using the specific solver (NB only euler and Cvode )
# SIMULATE FMU
## problems:
1. modifica dei parametri
2. funzionamento cooling