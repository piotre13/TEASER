__author__ = 'Pietro Rando Mazzarino'
__date__ = '2022/06/03'
__credits__ = ['Pietro Rando Mazzarino']
__email__ = 'pietro.randomazzarino@polito.it'

# clean code!


from OMPython import ModelicaSystem
import os
from OMPython import OMCSessionZMQ
import time
import memory_profiler as mp

# from memory_profiler import profile



@mp.profile
def Modelica2FMU(mo_name, mo_path, mo_lib, FMU_name, FMU_version="2.0", FMU_type="cs", commandLineOptions=None,
				 **kwargs):
	# instantiating the model and building it
	momodel = ModelicaSystem(mo_path, mo_name, mo_lib, commandLineOptions=commandLineOptions)
	momodel.buildModel()

	# setting the options/params and inputs if present
	if kwargs:
		for key in kwargs:
			if key == 'set_params':
				momodel.setParameters(kwargs[key])
			elif key == 'set_continous':
				momodel.setContinuous(kwargs[key])
			elif key == 'set_simOptions':
				momodel.setSimulationOptions(kwargs[key])
			elif key == 'set_linearOptions':
				momodel.setLinearizationOptions(kwargs[key])
			elif key == 'set_optOptions':
				momodel.setOptimizationOptions(kwargs[key])
			elif key == 'set_inputs':
				momodel.setInputs(kwargs[key])

	# creating FMU description
	description = {'quantities': momodel.getQuantities(),
				   'continous': momodel.getContinuous(),
				   'params': momodel.getParameters(),
				   # 'linear_params': momodel.getlinearParameters(),
				   'inputs': momodel.getInputs(),
				   'outputs': momodel.getOutputs(),
				   'sim_options': momodel.getSimulationOptions(),
				   'lin_options': momodel.getLinearizationOptions(),
				   'opt_options': momodel.getOptimizationOptions(),
				   # 'solutions': momodel.getSolutions()#could not work without simulate}
				   }

	# create & extract the FMU
	momodel.convertMo2Fmu(version=FMU_version, fmuType=FMU_type, fileNamePrefix=FMU_name, includeResources=True)
	log = momodel.getconn.sendExpression("getErrorString()")


@mp.profile
def clean_up(FMU_folder="."):
	files = [f for f in os.listdir(FMU_folder) if os.path.isfile(f)]
	acc_ext = ['.py', '.fmu', '.md', 'FMU.log', '.dat']
	for file in files:
		if not any([file.endswith(i) for i in acc_ext]):
			file = os.path.join(FMU_folder, file)
			os.remove(file)


@mp.profile
def main(mo_lib, prj_name, gen_mod_dir):
	mod_dir = os.path.join(gen_mod_dir, prj_name)
	mo_fullpath = os.path.join(mod_dir, 'package.mo')
	directories = [name for name in os.listdir(mod_dir) if os.path.isdir(os.path.join(mod_dir, name))]
	for dir_n in directories:
		mo_name = prj_name + "." + dir_n + "." + dir_n + "_Models." + dir_n + "_SingleDwelling"
		name = mo_name.split('.')[1] + '_linux'
		kwargs = {}
		# cmd_opt = '--fmiFlags=s:cvode'
		cmd_opt = None
		Modelica2FMU(mo_name, mo_fullpath, mo_lib, name, "2.0", commandLineOptions=cmd_opt, **kwargs)
	clean_up()


if __name__ == '__main__':
	omc = OMCSessionZMQ()
	omc.sendExpression("installPackage(AixLib, \"0.9.1\", exactMatch=true)")
	start = time.time()
	mo_lib = ["Modelica, {\"3.2.3\"}", "AixLib, {\"0.9.1\"}", ]  # "/home/pietrorm/Documents/CODE/TEASER/FMUs/Building2/package.mo" ]
	prj_name = 'tabula_ita_test_1'
	gen_mod_dir = '/media/space/rando/CODE/TEASER/TeaserOut/modelica'

	# REAL main no profiling
	main(mo_lib, prj_name, gen_mod_dir)

	end = time.time()
	print('Time taken to end the export fmu is: ', end - start)

	##PROFILING main only when profiling
	#res = mp.memory_usage((main, [mo_lib, prj_name, gen_mod_dir]), interval=.001, retval=True)
	#print('min mem', min(res[0]))
	#print('max mem', max(res[0]))
	#print('used mem', max(res[0]) - min(res[0]))
	#print('fun output', res[1])