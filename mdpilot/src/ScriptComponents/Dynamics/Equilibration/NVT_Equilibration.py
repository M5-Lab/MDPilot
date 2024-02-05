import EquilibrationScript


class NVT_Equilibration(EquilibrationScript):

    log_file_name = "nvt_log.txt"
    log_header = '"Temp"'

    def NVT_Equilibration(self, pilot : "Pilot", T_damp : float, T_start : float, n_steps : int, log_interval = 10000, T_end = None):

        self.T_damp = T_damp
        self.T_start = T_start
        self.n_steps = n_steps
        self.log_interval = log_interval

        if T_end is None:
            self.T_end = T_start

        pilot.add_variables(self, ["T_damp", "T_start", "T_end", "n_steps"])



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