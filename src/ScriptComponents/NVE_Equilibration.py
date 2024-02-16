from .EquilibrationScript import EquilibrationScript


class NVE_Equilibration(EquilibrationScript):

    log_file_name = "nve_log.txt"
    log_header = '"KE PE Temp"'

    def __init__(self, pilot : "Pilot", n_steps : int, log_interval = 10000):


        self.n_steps = n_steps
        self.log_interval = log_interval

        pilot.add_variables(self, ["n_steps"])


        #* would be nice to check that T_damp ~ 100*dt


    def generate_script_text(self):
        cmd = f"fix nve_equil_fix all nve\n"
        run = "\trun ${NVE_Equilibration_n_steps}\n"
        unfix = "unfix nvt_equil_fix\n"

        log = ""
        if self.log_interval is not None:
            if self.log_interval < self.n_steps:
                vars = "${thermo_ke} ${thermo_pe} ${thermo_temp}"
                log = f"\tfix nve_log all print {self.log_interval} \"{vars}\" screen no file {self.log_file_name} title {self.log_header}\n"
                unfix += f"unfix nve_log\n"
            else:
                raise Warning("Logging rate is greater than equilibration duration in NVE equilibration. Will not generate logs.")

        reset_timestep = "reset_timestep 0\n"

        return cmd + run + log + unfix + reset_timestep
