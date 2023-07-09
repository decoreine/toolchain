import subprocess
import sys
import os
import re
import shutil

def run_command(command):
    print(command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return process.returncode, stdout.decode().strip(), stderr.decode().strip()

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

def create_file(file_path, content):
    print("Create file : ",content)
    folder_path = os.path.dirname(file_path)
    os.makedirs(folder_path, exist_ok=True)
    with open(file_path, "w") as file:
        file.write(content)

def create_component(component_name, content):
    print("Create component : ",component_name)
    component_path = f"src/components/{component_name}.vue"
    with open(component_path, "w") as file:
        file.write(content)

def update_file(file_path, content):
    print("Update File : ",file_path)
    with open(file_path, "w") as file:
        file.write(content)

def replace_in_file(file_path, pattern, replacement):
    print ("Replace in file", file_path)
    with open(file_path, "r") as file:
        content = file.read()

    updated_content = re.sub(pattern, replacement, content)

    with open(file_path, "w") as file:
        file.write(updated_content)

def add_to_file(file_path, snippet):
    print ("Add to file", file_path)
    with open(file_path, "r+") as file:
        content = file.read()
        file.seek(0, 0)
        file.write(snippet + content)

# Check if Node.js is installed
return_code, stdout, stderr = run_command("node -v")
if return_code != 0 or not stdout.startswith("v"):
    print("Node.js is not installed. Please install Node.js before running this script.")
    sys.exit(1)

# Change working directory to the project folder
os.chdir("project")

# Install Tailwind for the project
run_command("npm install -D tailwindcss@latest postcss@latest autoprefixer@latest")
run_command("npm install -D tailwindcss@latest postcss@latest autoprefixer@latest")


# Create a new component
component_name = "Dashboard"
component_source = '''
<template>
  <div>
    <h1>Hello, Bootstrap and Vite!</h1>
    <button class="btn btn-primary">Primary button</button>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  // Component logic goes here
}
</script>

<style>
/* Component styles go here */
</style>
'''
create_component(component_name, component_source)

# Update a file
file_path = "src/App.vue"
file_content = '''
<template>
  <div>
    <h1>Welcome to My Vue App</h1>
    <Dashboard />
  </div>
</template>

<script>
import Dashboard from './components/Dashboard.vue'

export default {
  name: 'App',
  components: {
    Dashboard,
  },
  // Add any additional configuration or logic here
}
</script>

<style>
/* Add any component-specific styles here */
</style>
'''
update_file(file_path, file_content)

# Replace import statement in main.js
file_path = "src/main.js"
pattern = r"import App from './App.vue'"
replacement = "import App from './App.vue'\nimport 'bootstrap/dist/css/bootstrap.css'\n"
replace_in_file(file_path, pattern, replacement)

'''
# Replace base path in vite.config.ts in metronic only
file_path = "vite.config.ts"
pattern = r"/metronic8/vue/demo1/"
replacement = "/"
replace_in_file(file_path, pattern, replacement)
'''

file_path = "vite.config.js"
file_content = '''import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '~bootstrap': path.resolve(__dirname, 'node_modules/bootstrap'),
    },
  },
});'''
update_file(file_path, file_content)

file_path = "src/assets/scss/styles.scss"
content = '''
// Import all of Bootstrap's CSS
@import "~bootstrap/scss/bootstrap";
'''
create_file(file_path, content)


# Replace import statement in main.js
file_path = "src/main.js"
file_content = '''import { createApp } from 'vue'
import App from './App.vue'

// Import our custom CSS
//import './assets/scss/styles.scss'
import 'bootstrap/dist/css/bootstrap.css'

/**
*
// Import all of Bootstrap's JS
import * as bootstrap from 'bootstrap'
//You can also import JavaScript plugins individually as needed to keep bundle sizes down:
import Alert from 'bootstrap/js/dist/alert';

// or, specify which plugins you need:
import { Tooltip, Toast, Popover } from 'bootstrap';
*/
createApp(App).mount('#app')
'''
update_file(file_path, file_content)

