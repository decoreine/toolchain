import os
import json

from lib.dirs import *

class Build :
    def __init__(self):
        build_path = os.environ.get("PYLA_BUILD_PATH")
        
        controllers_path = os.environ.get("PYLA_CONTROLLERS_PATH")
        controllers_method = os.environ.get("PYLA_CONTROLLERS_METHOD")
        
        models_path = os.environ.get("PYLA_MODELS_PATH")
        models_method = os.environ.get("PYLA_MODELS_METHOD")

        views_path = os.environ.get("PYLA_VIEWS_PATH")
        views_method = os.environ.get("PYLA_VIEWS_METHOD")

        views_path = os.environ.get("PYLA_VIEWS_PATH")
        views_method = os.environ.get("PYLA_VIEWS_METHOD")
        
        routes_path = os.environ.get("PYLA_ROUTS_PATH") 
        routes_method = os.environ.get("PYLA_ROUTS_METHOD")
        
        config_path = os.environ.get("PYLA_CONFIG_PATH")
        config_method = os.environ.get("PYLA_CONFIG_METHOD")
        
        service_provider_path = os.environ.get("PYLA_SERVICE_PROVIDER_PATH")
        service_provider_method = os.environ.get("PYLA_SERVICE_PROVIDER_METHOD")
        
        modules = get_files_in_directory(build_path)

        for module in modules :
            _path = module.replace("{module_name}",module)
            print("hello -> ",_path)





        
        # Create the base path if it doesn't exist
