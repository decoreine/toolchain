def php_array_to_json(php_content) :
    .050
    # Rvxkheplace the PHP tags and curly braces with JSON equivalents
    #content = php_content.replace('<?php','').replace('return ','').replace('?>','').replace('array(','{').replace('),','},').replace('=>',':').replace('\'','"')
    content = php_content.replace('<?php','').replace('return ','').replace('?>','').replace('array(','{').replace('),','},').replace('=>',':')
    #content = replace_curly_braces_with_square_brackets(content)
    return content

def json_to_php_array(json_content) :
    # Replace the JSON tags and curly braces with PHP equivalents
    content = json_content.replace('{', 'array(').replace('}', ')').replace(':', '=>').replace('"', "'")
    content = "<?php\nreturn " . content
    return content

def remove_comment_lines_from_line(file_name):
  with open(file_name, 'r') as f:
    lines = f.readlines()

  new_lines = []
  for line in lines:
    if not line.startswith('//'):
      new_lines.append(line)
  return ''.join(new_lines)

def remove_comment_lines(content) :
    new_lines = []
    for line in content.splitlines():
        l = line.strip();
        if not l.startswith('//'):
            new_lines.append(line)
    ## parse the JSON string into a dictionary
    
    json_str = '\n'.join(new_lines)
    #json_str = replace_curly_braces_with_square_brackets(json_str)

    return json_str

def replace_curly_braces_with_square_brackets(json_str):
    # Replace curly braces with square brackets to create a JSON array
    json_str = "[" + json_str[1:-1] + "]"

    # Load the JSON string into a Python object
    try:
        obj = json.loads(json_str)
    except json.JSONDecodeError:
        return None
    
    # Convert any unnamed objects within arrays to named objects
    def convert_unnamed_to_named(obj):
        if isinstance(obj, list):
            new_list = []
            for item in obj:
                if isinstance(item, dict):
                    new_list.append({"item": item})
                else:
                    new_list.append(item)
            return new_list
        elif isinstance(obj, dict):
            for key, value in obj.items():
                obj[key] = convert_unnamed_to_named(value)
            return obj
        else:
            return obj
    
    obj = convert_unnamed_to_named(obj)
    
    # Convert the corrected Python object back to a JSON string
    return json.dumps(obj)

def setup_database(project_folder):
    print("Install python-dotenv use : conda install -c conda-forge python-dotenv")
    
    # Load the environment variables from the .env file
    env_file = ".env"
    env_path = os.path.join( ev.projects_folder,ev.project_name,env_file)

    load_dotenv(env_path)

    # Access environment variables
    db_connection = os.environ.get('DB_CONNECTION')
    db_host = os.environ.get('DB_HOST')
    db_port = os.environ.get('DB_PORT')
    db_database = os.environ.get('DB_DATABASE')
    db_username = os.environ.get('DB_USERNAME')
    db_password = os.environ.get('DB_PASSWORD')

    # Use the environment variables
    #print(f"DB connection: {db_connection}")
    #print(f"DB host: {db_host}")
    #print(f"DB port: {db_port}")
    #print(f"DB database: {db_database}")
    #print(f"DB username: {db_username}")
    #print(f"DB password: {db_password}")

    # Prompt the user to change the values
    db_connection = input(f"Current value of DB_CONNECTION is '{db_connection}'. Enter new value (or press Enter to keep current value): ") or db_connection
    db_host = input(f"Current value of DB_HOST is '{db_host}'. Enter new value (or press Enter to keep current value): ") or db_host
    db_port = input(f"Current value of DB_PORT is '{db_port}'. Enter new value (or press Enter to keep current value): ") or db_port
    db_database = input(f"Current value of DB_DATABASE is '{db_database}'. Enter new value (or press Enter to keep current value): ") or db_database
    db_username = input(f"Current value of DB_USERNAME is '{db_username}'. Enter new value (or press Enter to keep current value): ") or db_username
    db_password = input(f"Current value of DB_PASSWORD is '{db_password}'. Enter new value (or press Enter to keep current value): ") or db_password

    #os.environ.setdefault('DB_CONNECTION',db_connection)
    #os.environ.setdefault('DB_HOST',db_host)
    #os.environ.setdefault('DB_PORT',db_port)
    #os.environ.setdefault('DB_DATABASE',db_database)
    #os.environ.setdefault('DB_USERNAME',db_username)
    #os.environ.setdefault('DB_PASSWORD',db_password)

    # Replace values of database variables in .env file
    with open(env_path, 'r') as f:
        lines = f.readlines()

    with open(env_path, 'w') as f:
        DB_CONNECTION_found = False
        DB_HOST_found = False
        DB_PORT_found = False
        DB_DATABASE_found = False
        DB_USERNAME_found = False
        DB_PASSWORD_found = False
        for line in lines:
            if line.startswith('DB_CONNECTION='):
                line = f'DB_CONNECTION={db_connection}\n'
                DB_CONNECTION_found = True
            elif line.startswith('DB_HOST='):
                line = f'DB_HOST={db_host}\n'
                DB_HOST_found = True
            elif line.startswith('DB_PORT='):
                line = f'DB_PORT={db_port}\n'
                DB_PORT_found = True
            elif line.startswith('DB_DATABASE='):
                line = f'DB_DATABASE={db_database}\n'
                DB_DATABASE_found = True
            elif line.startswith('DB_USERNAME='):
                line = f'DB_USERNAME={db_username}\n'
                DB_USERNAME_found = True
            elif line.startswith('DB_PASSWORD='):
                line = f'DB_PASSWORD={db_password}\n'
                DB_PASSWORD_found = True
            f.write(line)
        # if ther is no line create one new
        if DB_CONNECTION_found == False :f.write(f'DB_CONNECTION={db_connection}\n')
        if DB_HOST_found == False :f.write(f'DB_HOST={db_host}\n')
        if DB_PORT_found == False :f.write(f'DB_PORT={db_port}\n')
        if DB_DATABASE_found == False :f.write(f'DB_DATABASE={db_database}\n')
        if DB_USERNAME_found == False :f.write(f'DB_USERNAME={db_username}\n')
        if DB_PASSWORD_found == False :f.write(f'DB_PASSWORD={db_password}\n')

