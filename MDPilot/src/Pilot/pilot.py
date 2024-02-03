import numpy as np


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


    script_ordering = {"Geometry" : 0, "Potential" : 1, "EquilibrationScript" : 2, "Simulation" : 3}
    def sort_script_components(self):
        pass
        #& TODO
        # parent_classes = [issubclass(sc)]
        # np.sort(self.script_components, key = lambda x: self.script_ordering[parent_classes[x]])


    def build_script(self):

        script = "# Variable Definitions:\n"

        for var_name in self.variables.keys():
            script += f"variable {var_name} equal {self.variables[var_name]}\n"

        script += "\n==========================================\n"

        self.sort_script_components()

        for script_component in self.script_components:
            script += script_component.generate_script_text()
            script += "\n==========================================\n"


        #& still need a way to define things like mass, timestep and other higher level sim params
