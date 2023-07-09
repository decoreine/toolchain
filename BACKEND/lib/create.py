import os
import json

from lib.dirs import *
from lib.extras import *

class Create :
    def __init__(self):
        
        modules_names = input("Enter the names of the modules (separated by commas): ").split(",")

        build_path = os.environ.get("PYLA_BUILD_PATH")

        # Create the base path if it doesn't exist
        if not os.path.exists(build_path):
            os.makedirs(build_path)        
        # Create a file for each module item and put the default content into it
        for module in modules_names:
            if(module in get_files_in_directory("models")):
                default_content = get_json_dictionary(f"models/{module}.json")
            else :
                # Read the content from the "default.json" file
                default_content = get_json_dictionary("config/model.json")
            file_path = os.path.join(build_path, f"{module}.json")
            with open(file_path, "w") as file:
                json.dump(default_content, file, indent=4)
        input("All module templates have been created. Fill the templates and press Enter to continue...")