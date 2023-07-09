#https://nwidart.com/laravel-modules/v1/installation-and-setup


import os
import shutil
import json

def floder_create(path):
    if os.path.exists(path):
        choice = input(f"The module '{os.path.basename(path)}' already exists. Do you want to overwrite it? (y/n): ")
        if choice.lower() != 'y':
            print(f"{os.path.basename(path)} folder  creation aborted.")
            return
        else:
            shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)

def folder_remove(path):
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
            print(f"Directory {path} was deleted successfully.")
    except OSError as e:
        print(f"Error deleting directory {path}: {e}")

def folder_copy(source_folder, destination_folder):
    # Check if the destination folder already exists
    if os.path.exists(destination_folder):
        overwrite = input("Destination folder already exists. Do you want to overwrite it? (y/n): ")
        if overwrite.lower() != 'y':
            print("Copy cancelled.")
            exit()
        else:
            shutil.rmtree(destination_folder)

    # Copy the repositories folder  to the destination folder
    shutil.copytree(source_folder, destination_folder)

    # Rename the destination folder
    os.rename(destination_folder, destination_folder)

    # Update the URL of the destination folder
    with open(os.path.join(destination_folder, 'url.txt'), 'w') as f:
        f.write(destination_folder)

    print(f"The folder {destination_folder} was created successfully.")

def folders_remove(paths):
    for path in paths:
        folder_remove(path)

def folders_create(paths):
    for path in paths:
        floder_create(path)

#get all files without extenstion
def get_files_in_directory(path):
    file_names = []
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            file_name = os.path.splitext(file)[0]
            file_names.append(file_name)
    return file_names

# Open the JSON file and read its contents into a string
def get_file_content(path):
    with open(path, 'r') as f:
        file_string = f.read()
    return file_string