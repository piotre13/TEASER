from fmpy import *

fmu = 'FMUs/RC_building.fmu'

dump(fmu)

result = simulate_fmu(fmu)

from fmpy.util import plot_result
plot_result(result)