
import datetime
import shutil

class Moduless:
    
    def __init__(self):
        self.modules = {}
        self.modules_path = "app/Modules"

    def create_module(self,module_name):
        strip_module_name = str(module_name).replace(' ','')

        module_path = os.path.join(self.base_path, strip_module_name)
        # Create module directory if it doesn't exist

        if os.path.exists(module_path):
            choice = input(f"The module '{module_name}' already exists. Do you want to overwrite it? (y/n): ")
            if choice.lower() != 'y':
                #print("Module creation aborted.")
                return
            else:
                shutil.rmtree(module_path)
        
        os.makedirs(module_path, exist_ok=True)

        # Create subdirectories
        subdirectories = ["Controllers","Models","Views","Routes","Migrations"]
        for subdir in subdirectories:
            subdir_path = os.path.join(module_path, subdir)
            os.makedirs(subdir_path, exist_ok=True)
            self.prompt_json()

        # Create example files in each subdirectory with default content
        self.create_files(module_path, subdirectories, module_name)

        print(f"Module '{module_name}' created successfully!")

    def create_files(self,module_path, subdirectories, module_name):
        strip_module_name = str(module_name).replace(' ','')
        for subdir in subdirectories:
            file_name = self.get_default_file_name(subdir, module_name)
            file_path = os.path.join(module_path, subdir, file_name)
            with open(file_path, "w") as file:
                file.write(self.get_default_content(subdir, module_name))

    def get_default_content(self,subdirectory, module_name):
        strip_module_name = str(module_name).replace(' ','')
        slug_module_name = module_name.lower().replace(" ", "_")
        if subdirectory == "Controllers":
            controller_logic_content = f"<?php\n\nnamespace App\Modules\{strip_module_name}\Controllers;\n\nuse App\Http\Controllers\Controller;\nuse App\Modules\{strip_module_name}\Models\{strip_module_name};\nuse Illuminate\Http\Request;\n\nclass {strip_module_name}Controller extends Controller\n{{\n\tpublic function index()\n\t{{\n\t\t${slug_module_name}s = {slug_module_name}::all();\n\n\t\treturn view('{strip_module_name}::{slug_module_name}s.index', compact('{slug_module_name}s'));\n\t}}\n\n\tpublic function create()\n\t{{\n\t\treturn view('{strip_module_name}::{slug_module_name}s.create');\n\t}}\n\n\tpublic function store(Request $request)\n\t{{\n\t\t${slug_module_name} = new {strip_module_name}();\n\t\t//${slug_module_name}->title = $request->input('title');\n\t\t//${slug_module_name}->content = $request->input('content');\n\t\t${slug_module_name}->save();\n\n\t\treturn redirect()->route('{slug_module_name}s.index');\n\t}}\n\n\tpublic function edit($id)\n\t{{\n\t\t${slug_module_name} = {strip_module_name}::findOrFail($id);\n\n\t\treturn view('{strip_module_name}::{slug_module_name}s.edit', compact('{slug_module_name}'));\n\t}}\n\n\tpublic function update(Request $request, $id)\n\t{{\n\t\t${slug_module_name} = {strip_module_name}::findOrFail($id);\n\t\t//${slug_module_name}->title = $request->input('title');\n\t\t//${slug_module_name}->content = $request->input('content');\n\t\t${slug_module_name}->save();\n\n\t\treturn redirect()->route('{slug_module_name}.index');\n\t}}\n\n\tpublic function destroy($id)\n\t{{\n\t\t${slug_module_name} = {strip_module_name}::findOrFail($id);\n\t\t${slug_module_name}->delete();\n\n\t\treturn redirect()->route('{slug_module_name}.index');\n\t}}\n}}"
            return f"{controller_logic_content}"
        elif subdirectory == "Models":
            declaration_logic_content = "\n\t//protected $connection = 'mysql';\n\t//protected $primaryKey = 'id';\n\t//protected $keyType = 'int';\n\t//public $incrementing = true;\n\t//public $timestamps = true;\n\t//protected $dateFormat = 'Y-m-d H:i:s';\n\t//protected $guarded = ['admin_only_field'];\n\t//protected $fillable = ['name', 'email', 'password'];\n\t//protected $hidden = ['password'];\n\t//protected $visible = [];\n\t//protected $casts = ['is_admin' => 'boolean', 'settings' => 'json'];\n"
            return f"<?php\n\nnamespace App\\Modules\\{strip_module_name}\\Models;\n\nuse Illuminate\\Database\\Eloquent\\Model;\n\nclass {strip_module_name}Model extends Model\n{{\n\tprotected $table = '{slug_module_name}_table';\n\t {declaration_logic_content} \n}}"
        elif subdirectory == "Views":
            views = {
                'index': f"<!DOCTYPE html>\n<html>\n<head>\n\t<title>Post</title>\n</head>\n<body>\n\t<!--h1>{{ $title }}</h1>\n\t<p>{{ $content }}</p-->\n</body>\n</html>",
                'create': '<h1>Create a New User</h1><p>Fill out the form below to create a new user.</p><form>...</form>',
                'edit': '<h1>Edit User Details</h1><p>Edit the details of the selected user.</p><form>...</form>',
            }
            return f"<!DOCTYPE html>\n<html>\n<head>\n\t<title>Post</title>\n</head>\n<body>\n\t<!--h1>{{ $title }}</h1>\n\t<p>{{ $content }}</p-->\n</body>\n</html>"
        elif subdirectory == "Migrations":
            return f"<?php\n\nuse Illuminate\\Database\\Migrations\\Migration;\nuse Illuminate\\Database\\Schema\\Blueprint;\nuse Illuminate\\Support\\Facades\\Schema;\n\nclass Create{strip_module_name}Table extends Migration\n{{\n\t/**\n\t * Run the migrations.\n\t *\n\t * @return void\n\t */\n\tpublic function up()\n\t{{\n\t\tSchema::create('{slug_module_name}_table', function (Blueprint $table) {{\n\t\t\t$table->increments('id');\n\t\t\t//$table->string('title');\n\t\t\t//$table->string('content');\n\t\t\t$table->timestamps();\n\t\t}});\n\t}}\n\n\t/**\n\t * Reverse the migrations.\n\t *\n\t * @return void\n\t */\n\tpublic function down()\n\t{{\n\t\tSchema::dropIfExists('{slug_module_name}_table');\n\t}}\n}}"
        elif subdirectory == "Provider":
            return f"<?php\n\nnamespace App\Modules\{strip_module_name};\n\nuse Illuminate\Support\ServiceProvider;\n\nclass {strip_module_name}ServiceProvider extends ServiceProvider\n{{\n\tpublic function register()\n\t{{\n\t\t// Register any bindings or services here\n\t}}\n\n\tpublic function boot()\n\t{{\n\t\t// Load routes and views here\n\t\t$this->loadRoutesFrom(__DIR__.'/Routes/routes.php');\n\t\t$this->loadViewsFrom(__DIR__.'/Resources/views', '{slug_module_name}');\n\n\t\t// This function will automatically load the migrations located in the specified directory, \n\t\t// allowing you to run them using the php artisan migrate command.\n\t\t$this->loadMigrationsFrom(__DIR__.'/Migrations', '{slug_module_name});\n\t}}\n}}\n\n/*\nIn the boot method of a Laravel service provider, you can use various functions to configure your module or perform any necessary setup. Some commonly used functions include:\n\n\tloadRoutesFrom: Loads routes from a file or directory. It registers the routes defined in the specified file or directory.\n\n\tloadViewsFrom: Registers views from a directory. It allows you to use the views in your module using the specified namespace.\n\n\tloadMigrationsFrom: Registers migrations from a directory. It automatically loads the migrations defined in the specified directory when running the migrate command.\n\n\tpublishes: Sets up the publishing of your module's assets, such as configuration files, views, and migrations. It allows users of your module to easily customize its behavior.\n\n\tregisterPolicies: Registers authorization policies. It allows you to define policies for your module's resources to control access based on certain conditions.\n\n\tmergeConfigFrom: Merges your module's configuration files with the main Laravel application's configuration. It allows you to provide default configuration values for your module.\n\n\tobserve: Registers model observers. It allows you to define observers that listen to specific events on your module's models.\n\n\tmacro: Registers macros on Laravel's container or other classes. It allows you to extend Laravel's functionality with custom macros.\n\n*/"
        else:
            return ""
    
    def get_default_file_name(self,subdir, module_name):
        strip_module_name = str(module_name).replace(' ','')
        slug_module_name = str(module_name).lower().replace(' ','_')

        if subdir == "Controllers":
            return f"{strip_module_name}{subdir[:-1]}.php"
        elif subdir == "Models":
            return f"{strip_module_name}.php"
        elif subdir == "Views":
            return f"{slug_module_name}.blade.php"
        elif subdir == "Migrations":
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"{timestamp}_create_{slug_module_name}_table.php"
        else:
            return

