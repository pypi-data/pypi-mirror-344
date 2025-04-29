import os
from ..template.startapp import get_init_content
from .startproject import create_file
from ..template.startproject import   get_helper_utilities_content, get_welcome_controller_contant

def makeapp_with_folder(base_dir: str):
    """Creates the folder and file structure."""
    folders = [
        "utils",
        "routes",
        "models",
        "tests",
        "schemas",
        "services",
      
    ]

    files = {
        f"{base_dir}/utils/__init__.py": "# Utility functions \n\n"+get_helper_utilities_content(),
        f"{base_dir}/routes/__init__.py": "#Welcome Controller  "+get_welcome_controller_contant(),
        f"{base_dir}/models/__init__.py": "#Register all the model here Example below \n\n#from .user_model import UserModel",
        f"{base_dir}/tests/__init__.py": "#Register all the test cases here Example below \n\n#from .user_test import UserTest",
        f"{base_dir}/schemas/__init__.py": "#Register all the Shemas here Example below \n\n#from .user_schema import UserSchema",
        f"{base_dir}/services/__init__.py": "#Register all the services here Example below \n\n#from .user_service import UserService",
        f"{base_dir}/__init__.py": "# Configuration file\n"+get_init_content()
    }

    # Create folders
    for folder in folders:
        os.makedirs(f"{base_dir}/{folder}", exist_ok=True)

    # Create files
    for file, content in files.items():
        create_file(file, content)
    
   

