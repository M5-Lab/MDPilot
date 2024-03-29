import sys, os
sys.path.append(os.path.expanduser(r"C:\Users\ejmei\repos\MDPilot"))

from src import Geometry, LJ, NVT_Equilibration, Pilot, Velocities


structure_path = "mnt/c/Users/ejmei/repos/MDPilot/examples/script_gen_test/initial_structure_LJ.data"
outpath = "/mnt/c/Users/ejmei/repos/MDPilot/examples/script_gen_test/mytest.txt"
dt = 2.0 #fs
T_damp = 100.0*dt
T = 300
n_steps = 1000000

p = Pilot()
p.set_units("real")
p.set_timestep(dt)


g = Geometry(structure_path)
pot = LJ(0.24037, 3.4, 8.5)
v = Velocities("NVT_Equilibration_T_start", True)
nvt = NVT_Equilibration(p, T_damp, T, n_steps)

p.add_scripts(g, pot, v, nvt)
p.build_script(outpath)