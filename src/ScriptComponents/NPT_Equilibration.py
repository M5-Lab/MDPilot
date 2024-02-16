from .EquilibrationScript import EquilibrationScript

class NPT_Equilibration(EquilibrationScript):

    log_file_name = "npt_log.txt"
    log_header = '"Temp Press PE KE"'

    def __init__(self, pilot : "Pilot", T_damp : float, P_damp : float,
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

        pilot.add_variables(self, ["T_damp", "T_start", "T_end", "P_damp", "P_start", "P_end", "n_steps"])


        #* would be nice to check that T_damp ~ 100*dt
        #* would be nice to check that P_damp ~ 1000*dt


    def generate_script_text(self):
        cmd = "fix npt_equil_fix all npt temp {NPT_Equilibration_T_start} {NPT_Equilibration_T_end} {NPT_Equilibration_T_damp} {NPT_Equilibration_P_type} {NPT_Equilibration_P_start} {NPT_Equilibration_P_end} {NPT_Equilibration_P_damp}\n"
        run = "\trun ${NPT_Equilibration_n_steps}\n"
        unfix = "unfix nvt_equil_fix\n"

        log = ""
        if self.log_interval is not None:
            if self.log_interval < self.n_steps:
                vars = "${thermo_temp} ${thermo_press} ${thermo_ke} ${thermo_pe}"
                log = f"\tfix npt_log all print {self.log_interval} \"{vars}\" screen no file {self.log_file_name} title {self.log_header}\n "
                unfix += f"unfix npt_log\n"
            else:
                raise Warning("Logging rate is greater than equilibration duration in NPT equilibration. Will not generate logs.")

        reset_timestep = "reset_timestep 0\n"

        return cmd + run + log + unfix + reset_timestep
        
