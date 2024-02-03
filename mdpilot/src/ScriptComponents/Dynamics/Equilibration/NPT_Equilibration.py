import EquilibrationScript

class NPT_Equilibration(EquilibrationScript):

    log_file_name = "npt_log.txt"
    log_header = '"Temp Press"'

    def NPT_Equilibration(self, pilot : "Pilot", T_damp : float, P_damp : float,
                          T_start : float, P_start : float, n_steps : int,
                          log_interval = 10000, T_end = None, P_end = None, P_type : str = "iso"):

        self.T_damp = T_damp
        self.T_start = T_start
        self.P_damp = P_damp
        self.P_start = P_start
        self.P_type = P_type

        self.n_steps = n_steps
        self.log_interval = log_interval
        

        if T_end is None:
            self.T_end = T_start

        if P_end is None:
            self.P_end = P_start

        self.log_file_name = "npt_log.txt"
        self.log_header = '"Temp Press"'

        pilot.add_variables(self, ["T_damp", "T_start", "T_end", "P_damp", "P_start", "P_end", "n_steps"])


        #* would be nice to check that T_damp ~ 100*dt
        #* would be nice to check that P_damp ~ 1000*dt


    def generate_script_text(self):
        cmd = f"fix npt_equil_fix all npt temp {self.T_start} {self.T_end} {self.T_damp} {self.P_type} {self.P_start} {self.P_end} {self.P_damp}\n"
        run = f"run {self.n_steps}\n"
        unfix = f"unfix nvt_equil_fix\n"

        log = ""
        if self.log_interval is not None:
            if self.log_interval > self.n_steps:
                vars = "${thermo_temp} ${thermo_press}"
                log = f"fix npt_log all print {self.log_interval} \"{vars}\" screen no file {self.log_file_name} title {self.log_header}\n "
            else:
                raise Warning("Logging rate is greater than equilibration duration in NVT equilibration. Will not generate logs.")

        return cmd + run + log + unfix
        
