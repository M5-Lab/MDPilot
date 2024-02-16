from .EquilibrationScript import EquilibrationScript


class NVE_Equilibration(EquilibrationScript):

    log_file_name = "nve_log.txt"
    log_header = '"PotEng"'

    def __init__(self, pilot : "Pilot", n_steps : int, log_interval = 10000):


        self.n_steps = n_steps
        self.log_interval = log_interval

        pilot.add_variables(self, ["n_steps"])


        #* would be nice to check that T_damp ~ 100*dt


    def generate_script_text(self):
        cmd = f"fix nvt_equil_fix all nvt temp {self.T_start} {self.T_end} {self.T_damp}\n"
        run = f"run {self.n_steps}\n"
        unfix = f"unfix nvt_equil_fix\n"

        log = ""
        if self.log_interval is not None:
            if self.log_interval > self.n_steps:
                vars = "${thermo_temp}"
                log = f"fix nvt_log all print {self.log_interval} \"{vars}\" screen no file {self.log_file_name} title {self.log_header}\n"
            else:
                raise Warning("Logging rate is greater than equilibration duration in NVT equilibration. Will not generate logs.")

        return cmd + run + log + unfix
