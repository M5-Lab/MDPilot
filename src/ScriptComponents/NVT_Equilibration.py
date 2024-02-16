from .EquilibrationScript import EquilibrationScript


class NVT_Equilibration(EquilibrationScript):

    log_file_name = "nvt_log.txt"
    log_header = '"KE PE Temp"'

    def __init__(self, pilot : "Pilot", T_damp : float, T_start : float, n_steps : int, log_interval = 10000, T_end = None):

        self.T_damp = T_damp
        self.T_start = T_start
        self.n_steps = n_steps
        self.log_interval = log_interval

        if T_end is None:
            self.T_end = T_start

        pilot.add_variables(self, ["T_damp", "T_start", "T_end", "n_steps"])

        #* would be nice to check that T_damp ~ 100*dt


    def generate_script_text(self):
        cmd = "fix nvt_equil_fix all nvt temp ${NVT_Equilibration_T_start} ${NVT_Equilibration_T_end} ${NVT_Equilibration_T_damp}\n"
        run = "\trun ${NVT_Equilibration_n_steps}\n"
        unfix = "unfix nvt_equil_fix\n"

        log = ""
        if self.log_interval is not None:
            if self.log_interval < self.n_steps:
                vars = "${thermo_ke} ${thermo_pe} ${thermo_temp}"
                log = f"\tfix nvt_log all print {self.log_interval} \"{vars}\" screen no file {self.log_file_name} title {self.log_header}\n"
                unfix += f"unfix nvt_log\n"
            else:
                raise Warning("Logging rate is greater than equilibration duration in NVT equilibration. Will not generate logs.")

        reset_timestep = "reset_timestep 0\n"

        return cmd + run + log + unfix + reset_timestep
