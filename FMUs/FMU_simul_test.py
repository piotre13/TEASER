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
import json
from utils import read_config

#todo GRANDE DOMANDA CONFRONTO CON DANIELE
#per quanto riguarda la descrizione dell'fmu ha senso leggersi il json associato o no secondo te?




class FmuSim ():
    def __init__(self, fmu_path,fmu_name, instance_name, config):
        self.model_description = read_model_description(fmu_path)
        self.unzipdir = extract(fmu_path)

        self.fmu = FMU2Slave(guid=self.model_description.guid,
                    unzipDirectory=self.unzipdir,
                    modelIdentifier=self.model_description.coSimulation.modelIdentifier,
                    instanceName=instance_name)

        #extract fmu description from json (inputs, outputs, params etc..)
        descr_file = config['paths']['FMU_descr_folder']+'/'+ fmu_name +'.json'
        with open(descr_file, 'r') as fp:
            self.description = json.load(fp)
            fp.close()

        self.vrs = {}
        self.inputs = list(self.description['inputs'].keys())
        self.outputs = list(self.description['outputs'].keys())


        for variable in self.model_description.modelVariables:
            self.vrs[variable.name] = variable.valueReference
            #se  non uso il json description posso tirarmi fuori le cose giocando con i nomi e.g. 'out' in variable.name

        print(self.outputs)


    def initialize(self, start_time, step_size, params, debugLog= 7):
        self.step_size = step_size # todo see if it must be passed or if is not used
        self.fmu.instantiate(loggingOn=debugLog)


        #self.fmu.setDebugLogging(loggingOn=debugLog)
        self.fmu.setupExperiment(startTime=start_time)

        #initialization mode
        self.fmu.enterInitializationMode()
        self.modify_param(params)
        #print('eccola qui:',self.fmu.getReal([self.vrs['h_heater']]))
        self.fmu.exitInitializationMode()

    def step(self, time, inputs):
        #phase1 set the inputs # todo check if values and keys are in the right order
        #vals = inputs.values()
        keys = list(inputs.keys())
        for key in keys:
            inp = inputs[key]
            if type(inp)== bool:
                self.fmu.setBoolean([self.vrs[key]],[inp])
            else:
                #self.fmu.setReal([self.vrs[key] for key in list(inputs.keys())], [inp for inp in list(inputs.values())])
                self.fmu.setReal([self.vrs[key]],[inp])


        #phase2 doStep
        print('eccola qui:', self.fmu.getReal([self.vrs['recOrSep']]))
        self.fmu.doStep(currentCommunicationPoint=time, communicationStepSize=self.step_size)
        print('eccola qui:', self.fmu.getReal([self.vrs['recOrSep']]))

        #phase2/3 getstatus todo check the status how is managed
        #status = self.fmu.getStatus()
        #realStatus = self.fmu.getRealStatus()

        #phase3 get outputs
        out = self.fmu.getReal([self.vrs[out]for out in self.outputs])
        return out

    def modify_param(self, kvals):
        keys_real=[]
        vals_real=[]
        keys_bool=[]
        vals_bool=[]
        for k, val in kvals.items():
            if isinstance(val, bool):
                keys_bool.append(self.vrs[k])
                if val:
                    vals_bool.append(val)
                else:
                    vals_bool.append(val)
            elif val!= None and not isinstance(val, bool):
                keys_real.append(self.vrs[k])
                vals_real.append(val)

        self.fmu.setReal(keys_real, vals_real)
        self.fmu.setBoolean(keys_bool,vals_bool)


    def finalize(self):
        self.fmu.terminate()
        self.fmu.freeInstance()
        # clean up
        shutil.rmtree(self.unzipdir, ignore_errors=True)

    def plot(self):
        pass


if __name__ == '__main__':

    #paths
    RC_fmu = '/home/pietrorm/Documents/CODE/TEASER/FMUs/Bui01_DE_linux.fmu'
    dump(RC_fmu)

    fmu_name = 'Bui01_DE'
    #PI_fmu = 'PI_TempController.fmu'
    meteo_test = '/home/pietrorm/Documents/CODE/TEASER/data/test_meteo.csv'
    dump(RC_fmu)
    config = read_config('/home/pietrorm/Documents/CODE/TEASER/config.yaml')
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
    #                'WindDir': None,
    #                'heaterActive':True,
    #                'coolerActive':False,
    #                }
    sim_opt = {
        'startTime': 0.0,
        'stopTime': 86400,
        'stepSize': 10,
        'sampling':'10s',
        'tolerance': 1e-06,
        'debugLog': 0,
    }

    Meteo = MeteoReader(meteo_test,8760,sim_opt['sampling'])
    FMUSim = FmuSim(RC_fmu,fmu_name, 'instance1', config)

#initialize fmu, in this stage is possible to modify some parameters
#do n
    params = {'h_cooler': None,
              'l_cooler': None,
              'h_heater': 0.0,#lo modifica ma non ha effetto (è parameter, fixed)
              'l_heater': None,
              'heaterCooler.h_cooler': None,
              'heaterCooler.l_cooler':None,
              'heaterCooler.h_heater':None, # non lo modifica ma non ha effetto (è calculated parameter, fixed)
              'heaterCooler.l_heater':None,
              'heaterCooler.staOrDyn':None,
              'recOrSep':False, # non lo modifica neanche (è calculated parameter, fixed)
              'heaterCooler.recOrSep':None,
              'Heater_on':None,
              'heaterCooler.Heater_on':None,
              'heaterCooler.zoneParam.HeaterOn':None,
              'Cooler_on':None,
              'heaterCooler.Cooler_on':None,
              'heaterCooler.zoneParam.CoolerOn:':None,
              'heaterCooler.zoneParam.HeaterOn:': None,
              'TThresholdCooler':None,
              'TThresholdHeater':None,
              'heaterCooler.zoneParam.TThresholdCooler':None,
              'heaterCooler.zoneParam.TThresholdHeater':None,
              'KR_cooler':None,
              'KR_heater':None,
              'heaterCooler.KR_cooler':None,
              'heaterCooler.KR_heater':None,
              'heaterCooler.pITempCool.KR':None,
              'heaterCooler.pITempHeat.KR':None,
              'heaterCooler.zoneParam.KRCool':None,
              'heaterCooler.zoneParam.KRHeat':None,
              'TN_cooler':None,
              'TN_heater':None,
              'heaterCooler.TN_cooler':None,
              'heaterCooler.TN_heater':None,
              'heaterCooler.pITempCool.TN':None,
              'heaterCooler.pITempHeat.TN':None,
              'heaterCooler.zoneParam.TNCool':None,
              'heaterCooler.zoneParam.TNHeat':None,




              }
    FMUSim.initialize(sim_opt['startTime'],sim_opt['stepSize'],params, sim_opt['debugLog'])



    inputs_keys = FMUSim.inputs
    inputs = {}
    t = sim_opt['startTime']
    index = 0
    outputs = []
    t0 = tmp.time()
    while t < sim_opt['stopTime']:
        for inp in inputs_keys:
            try:
                if inp == 'DryBulb':
                    inputs[inp] = Meteo.get_value(index, inp)
                else:
                    inputs[inp]=Meteo.get_value(index,inp)
            except:
                print('setting inputs outside meteo file')
                try:
                    if Meteo.get_value(index,'DryBulb')>= 400:
                        print('activating cooling')
                        inputs['heaterActive'] = 0
                        inputs['coolerActive'] = 1

                except:
                    print('exception2')
                    pass
                inputs['heaterActive'] = 1
                inputs['coolerActive'] = 0
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
    plt.plot([ou[2] for ou in outputs], label='T_air')
    plt.legend()
    plt.show()
    plt.close()
    #heating power
    plt.plot([ou[1]for ou in outputs], label='P_heating')
    plt.legend()
    plt.show()
    plt.close()
    #P_cooler
    plt.plot([ou[0] for ou in outputs], label='P_cooling')
    plt.legend()
    plt.show()
    plt.close()
#data inputs
#meteo = pd.read_csv(meteo_test)

#FMU dump
#dump(RC_fmu)
#dump(PI_fmu)


