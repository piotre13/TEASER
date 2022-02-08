from fmpy import read_model_description, extract
from fmpy.fmi2 import FMU2Slave
from fmpy.util import plot_result
import shutil


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

    def instantiate(self, instance_name='instance1'):
        model_description = read_model_description(self.fmu)

        #getting the model variables and their reference value
        self.vrs = {}
        for variable in model_description.modelVariables:
            self.vrs[variable.name] = variable.valueReference

        # create list of input and outputs
        # todo should standardize the creation of FMU having in var names '_input' and '_output' suffix
        self.inputs = []
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

        #actual simulation step
        self.fmu_inst.doStep(currentCommunicationPoint=time, communicationStepSize=step_size)

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

    fmu = 'FMUs/RC_building.fmu'
    start_time = 0.0
    threshold = 2.0
    stop_time = 2.0
    step_size = 1e-3

    instance_params = {
        'startTime' : start_time,
        'stopTime':stop_time,
        'tolerance':None
        }

    #instance of the fMU API class
    FMU_sim = SimulateFMU(fmu, **instance_params)

    #TODO in between instantiation and simulation at every step of the simulation should be a function populating the inputs

    #simulating
    time = start_time
    while time < stop_time:
        inputs = []
        FMU_sim.step(time, step_size, inputs)

        #updating time
        time += step_size
#    result = simulate_fmu(fmu, start_time = 0, stop_time = 1)

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