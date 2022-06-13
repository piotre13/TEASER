__author__ = 'Pietro Rando Mazzarino'
__date__ = '2022/06/03'
__credits__ = ['Pietro Rando Mazzarino']
__email__ = 'pietro.randomazzarino@polito.it'

from fmpy import read_model_description, extract, dump
from fmpy.fmi2 import FMU2Slave
import shutil
from fmpy.util import plot_result, download_test_file
import pandas as pd
from data.meteo_reader import MeteoReader
import matplotlib.pyplot as plt
import time as tmp

class FmuSim ():
    def __init__(self, fmu_path, instance_name):
        self.model_description = read_model_description(fmu_path)
        self.unzipdir = extract(fmu_path)

        self.fmu = FMU2Slave(guid=self.model_description.guid,
                    unzipDirectory=self.unzipdir,
                    modelIdentifier=self.model_description.coSimulation.modelIdentifier,
                    instanceName=instance_name)

        #extract model variables + inputs and outputs
        self.vrs = {}
        self.inputs = []
        self.outputs = []
        self.zoneparam = []
        for variable in self.model_description.modelVariables:
            self.vrs[variable.name] = variable.valueReference
            if variable.causality == 'input':
                self.inputs.append(variable.name)
            if 'zoneParam' in variable.name:
                self.zoneparam.append(variable.name)


        for out in self.model_description.outputs:
            self.outputs.append(out.variable.name)


    def initialize(self, start_time, step_size, debugLog= 7):
        self.step_size = step_size # todo see if it must be passed or if is not used
        self.fmu.instantiate(loggingOn=debugLog)
        #self.fmu.setDebugLogging(loggingOn=debugLog)
        self.fmu.setupExperiment(startTime=start_time)

        #initialization mode
        self.fmu.enterInitializationMode()
        #self.fmu.setReal([self.vrs[key] for key in ['heaterCoolerController.zoneParam.hHeat','heaterCooler.zoneParam.hHeat','h_heater']], [inp for inp in [1000,1000,1000]])

        self.fmu.exitInitializationMode()

    def step(self, time, inputs):
        #phase1 set the inputs # todo check if values and keys are in the right order
        vals = inputs.values()
        keys = inputs.keys()
        self.fmu.setReal([self.vrs[key] for key in list(inputs.keys())], [inp for inp in list(inputs.values())])
        #self.fmu.setReal([self.vrs[key] for key in ['heatCoolRoom_in']], [inp for inp in [1000.0]])


        #phase2 doStep

        self.fmu.doStep(currentCommunicationPoint=time, communicationStepSize=self.step_size)

        #phase2/3 getstatus todo check the status how is managed
        #status = self.fmu.getStatus()
        #realStatus = self.fmu.getRealStatus()

        #phase3 get outputs
        out = self.fmu.getReal([self.vrs[out]for out in self.outputs])
        return out

    def finalize(self):
        self.fmu.terminate()
        self.fmu.freeInstance()
        # clean up
        shutil.rmtree(self.unzipdir, ignore_errors=True)


if __name__ == '__main__':

    #paths
    RC_fmu = '/home/pietrorm/Documents/CODE/TEASER/FMUs/MyBuilding_noAct_noDyn.fmu'
    #PI_fmu = 'PI_TempController.fmu'
    meteo_test = '/home/pietrorm/Documents/CODE/TEASER/data/test_meteo.csv'
    dump(RC_fmu)

    #params
    # inputs_keys = {'Atmos_Pressure': None,
    #                'Ceiling_Hgt': None,
    #                'DewPoint': None,
    #                'DifHorzRad': None,
    #                'DirNormRad': None,
    #                'DryBulb': None,
    #                'HorzIRSky': None,
    #                'OpaqSkyCvr': None,
    #                'RelHum': None,
    #                'TotSkyCvr': None,
    #                'WindSpd': None,
    #                'WindDir': None
    #                }
    sim_opt = {
        'startTime': 0.0,
        'stopTime': 86400,
        'stepSize': 60,
        'sampling':'1min',
        'tolerance': None,
        'debugLog': 7,
    }

    Meteo = MeteoReader(meteo_test,8760,sim_opt['sampling'])
    FMUSim = FmuSim(RC_fmu, 'instance1')
    FMUSim.initialize(sim_opt['startTime'],sim_opt['stepSize'], sim_opt['debugLog'])
    inputs_keys = FMUSim.inputs
    inputs = {}
    print(FMUSim)
    t = sim_opt['startTime']
    index = 0
    outputs = []
    t0 = tmp.time()
    while t < sim_opt['stopTime']:
        for inp in inputs_keys:
            try:
                inputs[inp]=Meteo.get_value(index,inp)
            except:
                pass
        out = FMUSim.step(t,inputs)
        outputs.append(out)
        t+=sim_opt['stepSize']
        index+=1
    t1=tmp.time()
    print('simulation time: %s' %(t1-t0))
    FMUSim.finalize()
    #print(outputs)
    #T_air
    plt.plot([ou[2] for ou in outputs])
    plt.show()
    plt.close()
    #heating power
    plt.plot([ou[1]for ou in outputs])
    plt.show()
    plt.close()
    #P_cooler
    plt.plot([ou[0] for ou in outputs])
    plt.show()
    plt.close()
#data inputs
#meteo = pd.read_csv(meteo_test)

#FMU dump
#dump(RC_fmu)
#dump(PI_fmu)


