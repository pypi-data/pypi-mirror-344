# Import compiled extension
from pathlib import Path
import os
import sys

# Find the .so file in this directory
_module_dir = Path(__file__).parent
for file in os.listdir(_module_dir):
    if file.endswith('.so'):
        # Add the extension module directly
        from importlib.machinery import ExtensionFileLoader
        from importlib.util import spec_from_loader, module_from_spec
        
        _loader = ExtensionFileLoader('cuik_molmaker', str(_module_dir / file))
        _spec = spec_from_loader('cuik_molmaker', _loader)
        _module = module_from_spec(_spec)
        _loader.exec_module(_module)
        
        # Import all attributes from the module
        for attr in dir(_module):
            if not attr.startswith('_'):
                globals()[attr] = getattr(_module, attr)
        break
