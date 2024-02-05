import AbstractScriptComponent

class EquilbrationScript(AbstractScriptComponent):
   
    log_file_name = None
    log_header = None

    def __init_subclass__(cls, **kwargs):
        for required in ('log_file_name', 'log_header',):
            if not getattr(cls, required):
                raise TypeError(f"Can't instantiate class {cls.__name__} without {required} attribute defined")
        return super().__init_subclass__(**kwargs)
        
         
