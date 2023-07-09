import os
import shutil
import re

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

def folders_start_with(directory, key):  
    folders = []
    # Walk through the directory tree and collect all directories
    for dirpath, dirnames, filenames in os.walk(directory ):
        for dirname in dirnames:
            if(dirname.startswith(key)):
                folders.append(os.path.join(dirpath, dirname))
    return folders

def folders_except_start_with(folders, keep_folder):  
    deleted_folders = []
    for folder in folders:
        if os.path.basename(folder).startswith(keep_folder) == False and os.path.isdir(folder):
            deleted_folders.append(folder)
    return deleted_folders

def folders_except(folders, keep_folder):
    deleted_folders = []
    for folder in folders:
        if os.path.basename(folder) != keep_folder and os.path.isdir(folder):
            deleted_folders.append(folder)
    return deleted_folders

def folders_remove(folders):
    for folder in folders:
        folder_remove(folder)

def search_in_files(directory, word):
    file_paths = []

    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if os.access(file_path, os.R_OK):  # Check if the file is readable
                with open(file_path, 'r') as file:
                    try:
                        content = file.read()
                        if word in content:
                            file_paths.append(file_path)
                    except Exception as e:
                        pass
    return file_paths