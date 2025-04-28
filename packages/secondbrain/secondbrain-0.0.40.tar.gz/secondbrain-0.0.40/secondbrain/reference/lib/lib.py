import os
import sys
import importlib
import functools
import traceback
from .call_func import call_func

    
class ChangeDirectoryAndPath:
    """Context manager to change the current working directory and sys.path."""

    def __init__(self, module_path):
        self.module_path = module_path
        self.old_path = None

    def __enter__(self):
        self.old_path = os.getcwd()
        sys.path.insert(0, self.module_path)
        os.chdir(self.module_path)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.module_path in sys.path:
            sys.path.remove(self.module_path)
        os.chdir(self.old_path)
        

class ModuleManager:
    """Context manager for handling module imports and sys.modules state."""

    def __init__(self, module_path):
        self.module_path = module_path
        self.original_modules = sys.modules.copy()

    def __enter__(self):
        """Enter the runtime context related to this object."""
        self.change_dir = ChangeDirectoryAndPath(self.module_path)
        self.change_dir.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the runtime context related to this object."""
        self.change_dir.__exit__(exc_type, exc_value, traceback)
        self.cleanup_modules()

    def cleanup_modules(self):
        """Restore the original sys.modules state."""
        importlib.invalidate_caches()
        for key in list(sys.modules.keys()):
            if key not in self.original_modules:
                del sys.modules[key]
                

def wrapped_func(func, module_path):
    def _wrapped(*args, **kwargs):
        with ChangeDirectoryAndPath(module_path):
            try:
                result = call_func(func, args, kwargs)
            except Exception as e:
                print(f"Call function {func.__name__} error: {str(e)}")
                traceback.print_exc()
                raise
        return result
    
    wrapped_function = functools.wraps(func)(_wrapped)
    return wrapped_function

