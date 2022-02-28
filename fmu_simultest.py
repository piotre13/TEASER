from fmpy import read_model_description, extract
from fmpy.fmi2 import FMU2Slave
from fmpy.util import plot_result
import shutil
from fmpy import *
import matplotlib.pyplot as plt
import numpy as np


class SimulateFMU:
    def __init__(self, fmu, **kwargs):
        self.inputs = None  # list TODO maybe a dict
        self.outputs = {} # list TODO maybe a dict
        self.vrs = None  # dict
        self.unzipdir = None  # path

        self.fmu_inst = None  #fmu instance

        self.fmu = fmu  # fmu path
        self.kwargs = kwargs

        #run the instantiation can pass name of the instantiation
        self.instantiate()

        #testcollecting results
        self.T_air_ou = []
        self.T_ext = []

    def instantiate(self, instance_name='instance1'):
        model_description = read_model_description(self.fmu)

        #getting the model variables and their reference value
        self.vrs = {}
        for variable in model_description.modelVariables:
            self.vrs[variable.name] = variable.valueReference

        # create list of input and outputs
        # todo should standardize the creation of FMU having in var names '_input' and '_output' suffix
        #self.inputs = self.vrs['inputs']
        for out in model_description.outputs:
            name = out.variable.name
            self.outputs[name] = None

        #extract the FMU
        self.unzipdir = extract(self.fmu)

        self.fmu_inst = FMU2Slave(guid=model_description.guid,
                        unzipDirectory= self.unzipdir,
                        modelIdentifier=model_description.coSimulation.modelIdentifier,
                        instanceName=instance_name)

        self.fmu_inst.instantiate(loggingOn=7)
        self.fmu_inst.setupExperiment(**self.kwargs)
        self.fmu_inst.enterInitializationMode()
        #TODO can add some parametr initialization i thing
        self.fmu_inst.exitInitializationMode()

    def step(self, time, step_size, inputs):
        #setting inputs
        self.fmu_inst.setReal([self.vrs['DryBulb']], [inputs])

        #actual simulation step
        try:
            self.fmu_inst.doStep(currentCommunicationPoint=time, communicationStepSize=step_size)
            outputs4 = self.fmu_inst.getReal([self.vrs['Tair_ou'],self.vrs['weaBus.TDryBul']])
            self.T_air_ou.append(outputs4[0])
            self.T_ext.append(outputs4[1])
            print(outputs4)
        except:
            print('NOT WORKINGGGGG!')
            shutil.rmtree(self.unzipdir, ignore_errors=True)
        #gathering outputs and saving results

    def terminate(self):
        self.fmu_inst.terminate()
        self.fmu_inst.freeInstance()

        # clean up
        shutil.rmtree(self.unzipdir, ignore_errors=True)

    def _get_inputs_names(self):
        return self.inputs.keys()

    def _get_outputs_names(self):
        return self.outputs.keys()

    def _get_vars_names(self):
        return self.vrs.keys()



if __name__ == '__main__':

    fmu = 'FMUs/RC_building_HeatCool.fmu'
    dump(fmu)

    start_time = 0.0
    threshold = 2.0
    stop_time = 8760
    step_size = 60

    instance_params = {
        'startTime' : start_time,
        'stopTime':stop_time,
        'tolerance':None
        }

    #instance of the fMU API class
    FMU_sim = SimulateFMU(fmu, **instance_params)
    T_ext = list(np.linspace(283.15,300.15,8760))
    #TODO in between instantiation and simulation at every step of the simulation should be a function populating the inputs

    input_keys = ['Atmos_Pressure', 'Ceiling_Hgt', 'DewPoint', 'DifHorzRad', 'DirNormRad', 'DryBulb', 'HorzIRSky', 'OpaqSkyCvr', 'RelHum', 'TotSkyCvr', ]
    #simulating
    time = start_time
    i =0
    while time < stop_time:
        inputs = T_ext[i]
        FMU_sim.step(time, step_size, inputs)

        #updating time
        time += step_size
        i+=1
#    result = simulate_fmu(fmu, start_time = 0, stop_time = 1)
    plotting_value =  FMU_sim.T_air_ou
    print(len(plotting_value))
    print(plotting_value)
    plt.plot(plotting_value)
    plt.show()
    plt.close()
    plt.plot(FMU_sim.T_ext)
    plt.show()

#    from fmpy.util import plot_result
#    plot_result(result)


    '''possible simulation parameters in simulate_fmu() method
    filename,
                 validate: bool = True,
                 start_time: Union[float, str] = None,
                 stop_time: Union[float, str] = None,
                 solver: str ='CVode',
                 step_size: Union[float, str] = None,
                 relative_tolerance: Union[float, str] = None,
                 output_interval: Union[float, str] = None,
                 record_events: bool = True,
                 fmi_type: str = None,
                 start_values: Dict[str, Any] = {},
                 apply_default_start_values: bool = False,
                 input: np.ndarray = None,
                 output: Sequence[str] = None,
                 timeout: Union[float, str] = None,
                 debug_logging: bool = False,
                 visible: bool = False,
                 logger: Callable = None,
                 fmi_call_logger: Callable[[str], None] = None,
                 step_finished: Callable[[float, Recorder], bool] = None,
                 model_description: ModelDescription = None,
                 fmu_instance: _FMU = None,
                 set_input_derivatives: bool = False,
                 remote_platform: str = 'auto',
                 early_return_allowed: bool = False,
                 use_event_mode: bool = False
                 
    possible params for setupExperiment() method
        tolerance=None, startTime=0.0, stopTime=None
    '''