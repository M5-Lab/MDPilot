import mdpilot
from inspect import getmembers, isfunction


print(help(mdpilot))
# from mdpilot import Pilot, LJ, Geometry, NVT_Equilibration, EquilibrationAnalysis


# structure_path = "./LJ_4UC.data"
# outpath = "."
# dt = 2.0 #fs
# T_damp = 100.0*dt
# T = 300
# n_steps = 1000000

# p = Pilot()

# p.add_script(Geometry(structure_path))
# p.add_script(LJ(0.24037, 3.4, 8.5))
# p.add_script(NVT_Equilibration(p, T_damp, T, n_steps))

# p.build_script(outpath)