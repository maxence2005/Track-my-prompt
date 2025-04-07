import os
import importlib.util
import sys

# -------------------------------
# PROJECT PATH CONFIGURATION
# -------------------------------

# Root path of the project
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
project_root = os.path.join(project_root, 'track_my_prompt')

if project_root not in sys.path:
    sys.path.insert(0, project_root)

# -------------------------------
# MODULE LOADING
# -------------------------------

def _load_module(module_name, module_path):
    if os.path.exists(module_path):
        try:
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print(f"✅ Module {module_name} chargé avec succès.")
            return module
        except ModuleNotFoundError as e:
            print(f"❌ Erreur lors du chargement du module {module_name} : {e}")
            raise
        except AttributeError as e:
            print(f"❌ Erreur lors du chargement du module {module_name} : {e}")
            raise
    else:
        print(f"❌ Le module {module_name} n'existe pas à l'emplacement {module_path}")
        raise FileNotFoundError(f"Module {module_name} introuvable.")
    
def load(classe, type, file):
    """Loads a module

    Args:
        classe (Class): The class you load
        type (str): Class type (models, controller, etc.)
        file (str): File path

    Raises:
        AttributeError: Sends an error if the class isn't found

    Returns:
        Class: The loaded class
    """
    file_without_py = os.path.splitext(file)[0]
    module_full_path = os.path.join(project_root, type, file)
    module = _load_module(file_without_py, module_full_path)
    return_class = getattr(module, classe, None)
    if not return_class:
        raise AttributeError(f"La classe {classe} n'a pas été trouvée dans le module {file_without_py}.")
    return return_class