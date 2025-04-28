import importlib
import pkgutil
import os
import sys

def import_submodules(package_name):
    """Import all submodules of a package recursively."""
    package = importlib.import_module(package_name)
    
    for loader, name, is_pkg in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
        if is_pkg:
            import_submodules(name)
        else:
            importlib.import_module(name)

def discover_tools(folders: list[str] = None):
    """Discover and import all agent or utility modules to register their tools."""

    # Ensure the current directory is in sys.path
    current_dir = os.getcwd()
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    # Import all modules from the given folders
    for folder in folders:
        try:
            import_submodules(folder)
        except Exception as e:
            print(f"Warning: Could not import modules from {folder}: {e}")
