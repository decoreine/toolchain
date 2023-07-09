from dotenv import load_dotenv, find_dotenv,dotenv_values,set_key
from dotenv.main import DotEnv

def update_env_properties(env_file_path, properties):
    print("Install python-dotenv use : conda install -c conda-forge python-dotenv")

    env_data = dotenv_values(env_file_path)

    for prop in properties:
        if prop in env_data.keys():
            old_value = env_data[prop]
            input_value = input(f"Enter new value for {prop} (current value: {old_value}): ")
            if input_value:
                set_key(env_file_path, prop, input_value)
        else:
            input_value = input(f"Enter value for new property {prop}: ")
            if input_value:
                set_key(env_file_path, prop, str(input_value))

    print("Properties updated successfully.")