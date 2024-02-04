import numpy as np
import AnalysisComponent as AnalysisComponent
from typing import List

from ..ScriptComponents import EquilibrationScript
from ..FileIO.ParsingStrategies import FixPrintParser

class EquilibrationAnalysis(AnalysisComponent):
    
    def __init__(self, eq_script_comp : EquilibrationScript):
       self.eq_script_comp = eq_script_comp
       self.property_names = eq_script_comp.log_header.split()

    def get_equilibration_properties(self):
        return FixPrintParser(self.eq_script_comp.log_file_name).parse()

    def is_equilibrated(self, targets: List[float], tols : List[float]):
        """
        Args:
            targets: 
            tol: tolerance for equilibration
        """

        properties = self.eq_script_comp.get_equilibration_properties()

        is_equilibrated = {prop_name : 0 for prop_name in self.property_names}

        for i, property_name in enumerate(self.property_names):
            property = properties[property_name]
            samples = len(property)
            prop_cum = np.abs(np.cumsum(property) / (np.arange(samples) + 1) - targets[i])
            is_equilibrated[property_name] = np.all(prop_cum[int(0.9*samples):] < tols[i]) # at least last 10% of the time series are near target value within tolerance

        return is_equilibrated 
 
