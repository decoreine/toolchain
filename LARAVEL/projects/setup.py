from dir_functions import *
from env_functions import *

class ev :
    # Load environment variables from .env file
    env_path = os.path.join(os.path.dirname(__file__), '.env')

    load_dotenv(env_path)

    repositories_folder = os.environ.get('REPOSITORIES_PATH')
    projects_folder = os.environ.get('PROJECT_PATH')
    
    project_name = ""
    project_folder = ""
    laravel_env_path = ""
    def load_env() :
        if ev.repositories_folder == "" :
            ev.repositories_folder = input("PATH of the repositories folder: ")    
        if ev.projects_folder == "" :
            ev.projects_folder = input("PATH of the destination folder: ")
        if ev.project_name == "" :
            ev.project_name = input("Project Name: ")
        if ev.project_folder == "" :
            ev.project_folder = os.path.join(ev.projects_folder, ev.project_name)
        ev.laravel_env_path = os.path.join( ev.projects_folder,ev.project_name,'.env')

def keep_one_demo(name):
    folders = folders_start_with(ev.project_folder, "demo")
    folders = folders_except_start_with(folders, "demos")
    folders = folders_except(folders, name)
    folders_remove(folders)

def add_menu() :
    # Open the PHP file for reading
    file_path = 'C:\www\dashboard\config\global\menu.php'

    
#    with open(file_path, 'r') as file:
#        lines = file.readlines()
#
#    # Locate the array variable in the file
#    start_index = None
#    end_index = None
#    for i, line in enumerate(lines):
#        if "$array =" in line:
#            start_index = i
#        if start_index is not None and ")," in line:
#            end_index = i
#            break

#    # Add a new element to the array
#    new_element = "\n\tarray(\n\t\t'title' => 'New Item',\n\t\t'path' => 'new-item',\n\t),\n"
#    if start_index is not None and end_index is not None:
#        # The array variable was found
#        lines.insert(end_index, new_element)
#    else:
#        # The array variable was not found, so add it at the end of the file
#        lines.append("\n$array = array(\n\t" + new_element.lstrip() + ");\n")

#    # Write the updated file back
#    with open(file_path, 'w') as file:
#        file.writelines(lines)

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Find the index of the line that contains "// System"
    system_index = -1
    for i, line in enumerate(lines):
        if '// System' in line:
            system_index = i
            break

    # Insert the new code before the "// System" line
    if system_index >= 0:
        new_code = '''
        //Costumer MANAGER
        array(
            'title'      => 'Costumer MANAGER',
            'icon'       => array(
                'svg'  => theme()->getSvgIcon("demo1/media/icons/duotune/communication/com006.svg", "svg-icon-2"),
                'font' => '<i class="bi bi-person fs-2"></i>',
            ),
            'classes'    => array('item' => 'menu-accordion'),
            'attributes' => array(
                "data-kt-menu-trigger" => "click",
            ),
            'sub'        => array(
                'class' => 'menu-sub-accordion menu-active-bg',
                'items' => array(
                    array(
                        'title'  => 'Listing',
                        'path'   => 'customers/listing',
                        'bullet' => '<span class="bullet bullet-dot"></span>',
                    ),
                    array(
                        'title'  => 'Details',
                        'path'   => 'customers/details',
                        'bullet' => '<span class="bullet bullet-dot"></span>',
                    )
                ),
            ),
        ),\n
'''

        lines.insert(system_index, new_code)

    # Open the file for writing and write the modified content
    with open(file_path, 'w') as f:
        f.writelines(lines)



#-------------------- main function ----------------------------
if __name__ == "__main__":
    ev.load_env()

    ## Get the destination folder URL from the user
    #if input("Do you want to create new project? (y/n): ").lower() == 'y':
    #    folder_copy(ev.repositories_folder, ev.project_folder)

    #if input("Do you want to keep one demo ? (y/n): ").lower() == 'y':
    #    demo = input("What is the name of the demo you want to keep? : ")
    #    keep_one_demo(demo)
            
    #if input("Do you want to set up database properties? (y/n): ").lower() == 'y':
    #    #setup_database(ev.project_folder)
    #    db_properties = ['DB_CONNECTION','DB_HOST', 'DB_PORT', 'DB_DATABASE','DB_USERNAME','DB_PASSWORD']
    #    update_env_properties(ev.laravel_env_path, db_properties)

    #if input("Do you want to set up google properties? (y/n): ").lower() == 'y':
    #    db_properties = ['GOOGLE_CLIENT_ID','GOOGLE_CLIENT_SECRET', 'GOOGLE_CLIENT_CALLBACK']
    #    update_env_properties(ev.laravel_env_path, db_properties)


    files = search_in_files(ev.repositories_folder,'demo1')
    print(files)
    #add_menu()
