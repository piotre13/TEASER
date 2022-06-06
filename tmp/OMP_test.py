from OMPython import OMCSessionZMQ
omc = OMCSessionZMQ()
omc.sendExpression('getVersion()')
omc.sendExpression("loadModel(Modelica)")
from OMPython import ModelicaSystem

mod= ModelicaSystem('/home/pietrorm/Documenti/CODE/TEASER/TeaserOut/modelica/aixlib/PRJ_test/package.mo', 'PRJproject')

print(mod.getInputs())
print(omc)