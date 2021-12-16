from OMPython import OMCSessionZMQ
omc = OMCSessionZMQ()
omc.sendExpression('getVersion()')
omc.sendExpression("loadModel(Modelica)")
from OMPython import ModelicaSystem

mod= ModelicaSystem('/home/pietrorm/Documenti/CODE/TEASER/TeaserOut/modelica/aixlib/PRJ_test/package.mo', 'PRJproject')

print(mod.getInputs())
print(omc)

''' TODO here i should take only one model of a building and export it as a FMU
in addition test a stepped simulation with the exchange of inputs and outputs'''