import sys, os
sys.path.append(os.path.expanduser(r"C:\Users\ejmei\repos\MDPilot"))

from src import Geometry, LJ, NVT_Equilibration, Pilot


structure_path = "C:/Users/ejmei/repos/MDPilot/examples/script_gen_test/initial_structure_LJ.data"
outpath = "C:/Users/ejmei/repos/MDPilot/examples/script_gen_test/mytest.txt"
dt = 2.0 #fs
T_damp = 100.0*dt
T = 300
n_steps = 1000000

p = Pilot()
p.set_timestep(dt)
p.set_units("real")

g = Geometry(structure_path)
pot = LJ(0.24037, 3.4, 8.5)
nvt = NVT_Equilibration(p, T_damp, T, n_steps)

p.add_scripts(g, pot, nvt)
p.build_script(outpath)