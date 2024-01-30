from abc import ABC, abstractmethod

class AbstractScriptComponent(ABC):

    @abstractmethod
    def generate_script_text(self):
        """
        Geneartes a string that could be copied into a LAMMPS input-file
        """
        pass
