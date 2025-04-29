from __future__ import annotations
import sys
from pathlib import Path
from config import ConfigMeta
from setting import Setting

if getattr(sys, 'frozen', False):   # we are running in executable mode
    STD_DIR = Path(sys.argv[0]).parent
    print(f'Exe detected, working directory: {STD_DIR}')
else:   # we are running in a normal Python environment
    STD_DIR = Path(__file__).parent


class DirectoriesConfigMeta(ConfigMeta):
    @classmethod
    def _handle_key_value(cls, key, value):
        if isinstance(value, type):
            if issubclass(value, DirectoriesConfig):
                setattr(cls, key, value())
            
        if isinstance(value, Setting):
            raise TypeError(f'Values of {type(cls)} can only be of type Path or inherit ConfigMeta.\nGiven {key}: {type(value).__name__}({repr(value)})')

        if isinstance(value, Path):
            value.mkdir(exist_ok=True)
            setattr(cls, key, value)

        setattr(cls, 'STD_DIR', STD_DIR)
        super()._handle_key_value(key, value)
        

class DirectoriesConfig(metaclass=DirectoriesConfigMeta):
    pass