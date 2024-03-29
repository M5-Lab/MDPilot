import os

# Core novelty of this library
# Given an interface with a ScriptComponents object, PostProcess object, and Campaign object
# Will automatically determine initial and (if needed) future workflows to meet objective of campaign object

class Pilot:

    def __init__(self):
        self.script_components = []
        self.variables = {}
        self.units_set = False

        self.script = ""
    
    def add_variables(self, obj, var_list):
        for var in var_list:
            self.variables[f"{obj.__class__.__name__}_{var}"] = eval(f"obj.{var}")

    def set_timestep(self, dt : float):
        if self.units_set:
            self.script += f"timestep {dt}\n"

    def set_units(self, units : str):
        if units not in ["real", "lj", "metal", "si", "cgs", "electron", "micro", "nano"]:
            raise ValueError(f"Unknonw unit type for LAMMPS: {units}.")
        self.units_set = True
        self.script += f"units {units}\n"

    def add_script(self, script_component : "AbstractScriptComponent"):
        self.script_components.append(script_component)

    def add_scripts(self, *script_components : "AbstractScriptComponent"):
        for sc in script_components:
            self.add_script(sc)

    script_ordering = {"Geometry" : 0, "Potential" : 1, "EquilibrationScript" : 2, "Simulation" : 3}
    def sort_script_components(self):
        pass
        #& TODO
        # parent_classes = [issubclass(sc)]
        # np.sort(self.script_components, key = lambda x: self.script_ordering[parent_classes[x]])


    def build_script(self, out_path : str):

        
        if os.path.exists(out_path):
            raise ValueError(f"File {out_path} already exists. Please delete or rename it.")

        self.script += "\n# Variable Definitions:\n"

        for var_name in self.variables.keys():
            self.script += f"variable {var_name} equal {self.variables[var_name]}\n"

        self.script += "\n#==========================================#\n\n"


        self.sort_script_components()

        for script_component in self.script_components:
            self.script += script_component.generate_script_text()
            self.script += "\n#==========================================#\n\n"

        with open(out_path, "w") as f:
            f.write(self.script)

        #&where to set atom masses if not read in by geometry file?
