import os

# Core novelty of this library
# Given an interface with a ScriptComponents object, PostProcess object, and Campaign object
# Will automatically determine initial and (if needed) future workflows to meet objective of campaign object

class Pilot:

    def __init__(self):
        self.script_components = []

        self.variables = {}
    
    def add_variables(self, obj, var_list):
        for var in var_list:
            self.variables[f"{obj.__class__.__name__}_{var}"] = eval(f"obj.{var}")

    def set_timestep(self, dt):
        self.variables["timestep"] = dt

    def add_script(self, script_component : "AbstractScriptComponent"):
        self.script_components.append(script_component)


    script_ordering = {"Geometry" : 0, "Potential" : 1, "EquilibrationScript" : 2, "Simulation" : 3}
    def sort_script_components(self):
        pass
        #& TODO
        # parent_classes = [issubclass(sc)]
        # np.sort(self.script_components, key = lambda x: self.script_ordering[parent_classes[x]])


    def build_script(self, out_path : str):

        if os.path.exists(out_path):
            raise ValueError(f"File {out_path} already exists. Please delete or rename it.")

        script = "# Variable Definitions:\n"

        for var_name in self.variables.keys():
            script += f"variable {var_name} equal {self.variables[var_name]}\n"

        script += "\n==========================================\n"

        self.sort_script_components()

        for script_component in self.script_components:
            script += script_component.generate_script_text()
            script += "\n==========================================\n"

        with open(out_path, "w") as f:
            f.write(script)

        #&where to set atom masses if not read in by geometry file?
