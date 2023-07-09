import os
from lib.extras import *

class Config :
    def __init__(self):
        self.global_dictionary = get_json_dictionary('config/config.json')

        self.level = self.choose_the_level()

        levels = get_json_value_by_key(self.global_dictionary, "levels")
        
        self.level_dictionary = get_json_value_by_key(levels, self.level)
        self.level_string = get_json_string_value_by_key(levels, self.level)

        os.environ["PYLA_LEVEL_DICTIONARY"] = self.level_string

        self.build_path = get_json_value_by_key(self.global_dictionary,"build_path")
        os.environ["PYLA_BUILD_PATH"] = self.build_path

        self.modules_path = get_json_value_by_key(self.global_dictionary,"modules_path")
        os.environ["PYLA_MODULES_PATH"] = self.modules_path

        sub_directories = get_json_value_by_key(self.level_dictionary,"sub_directories")

        self.controllers = sub_directories.get("Controllers")
        os.environ["PYLA_CONTROLLERS_PATH"] = self.controllers.get("path")
        os.environ["PYLA_CONTROLLERS_METHOD"] = self.controllers.get("method")
        
        self.models = sub_directories.get("Models")
        os.environ["PYLA_MODELS_PATH"] = self.models.get("path")
        os.environ["PYLA_MODELS_METHOD"] = self.models.get("method")

        self.views = sub_directories.get("Views")
        os.environ["PYLA_VIEWS_PATH"] = self.views.get("path")
        os.environ["PYLA_VIEWS_METHOD"] = self.views.get("method")

        self.migrations = sub_directories.get("Migrations")
        os.environ["PYLA_VIEWS_PATH"] = self.views.get("path")
        os.environ["PYLA_VIEWS_METHOD"] = self.views.get("method")
        
        self.routes = sub_directories.get("Routes")
        os.environ["PYLA_ROUTS_PATH"] = self.routes.get("path")
        os.environ["PYLA_ROUTS_METHOD"] = self.routes.get("method")
        
        self.config = sub_directories.get("Config")
        os.environ["PYLA_CONFIG_PATH"] = self.config.get("path")
        os.environ["PYLA_CONFIG_METHOD"] = self.config.get("method")
        
        self.service_provider = sub_directories.get("ServiceProvider")
        os.environ["PYLA_SERVICE_PROVIDER_PATH"] = self.service_provider.get("path")
        os.environ["PYLA_SERVICE_PROVIDER_METHOD"] = self.service_provider.get("method")
        
    def choose_the_level(self):
        id_keys = []
        for index, key in enumerate(self.global_dictionary.get("levels").keys(), 1):
            id_key = f"[{index}]{key}"
            id_keys.append(id_key)
            print(f"{index}. {id_key}")

        if not id_keys:
            print("No keys found.")
            return None

        while True:
            try:
                choice = int(input("Enter the number of the configuration: "))
                if 1 <= choice <= len(id_keys):
                    return list(self.global_dictionary.get("levels").keys())[choice - 1]
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid choice. Please enter a valid number.")



#packages = Packages()
