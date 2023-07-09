import os
import json
from lib.blocks import *
from lib.extras import *


JSON_TYPE = ["json","list","array"]
IMAGE_TYPE = ["avatar","image"]

class Module:
    def json_interpret(self):
        while True:
            json_input = input(f"Enter a valide json ('JSON URL Or JSON Content') : ")
            try:
                self.data = json.loads(json_input)

                self.attributes = {}  # read all attributes and convert all attribute to dict value
                self.fillables = self.data.get('fillables', [])
                self.guardeds = self.data.get('guardeds', [])
                self.hiddens = self.data.get('hiddens', [])
                self.visibles = self.data.get('visibles', [])
                self.migration = self.data.get('migration', {})
                self.model = self.data.get('model', {})
                self.controller = self.data.get('controller', [])

                self.controller_headers = self.controller["headers"]
                self.controller_extends = self.controller["extends"]
                self.controller_blocks = self.controller["blocks"]
                self.controller_validators = self.controller.get('validators', [])

                self.model_headers = self.model["headers"]
                self.model_extends = self.model["extends"]
                self.model_uses = self.model["uses"]

                
                self.migration_headers = self.migration["headers"]
                self.migration_extends = self.migration["extends"]

                _attributes = self.data.get('attributes', [])

                #convert all attribute to dict value
                """
                for key, item  in _attributes.items() :
                    _item = {}
                    if isinstance(item, dict):
                        #if dict is difintion of field get the type from type attribute else return json
                        if "type" in item:
                            _item["type"] = item.get("type")
                            if "incremental" in item:
                                _item["incremental"] = item.get("incremental")
                            else:
                                _item["incremental"] = False 
                            if "unique" in item:
                                _item["unique"] = item.get("unique")
                            else:
                                _item["unique"] = False
                            if "nullable" in item:
                                _item["nullable"] = item.get("nullable")
                            else:
                                _item["nullable"] = False 
                            _item["foreign"] = item.get("foreign")
                            self.attributes[key] = _item

                        else:
                            _item["type"] = "json"
                            if "incremental" in item:
                                _item["incremental"] = item.get("incremental")
                            else:
                                _item["incremental"] = False 
                            if "unique" in item:
                                _item["unique"] = item.get("unique")
                            else:
                                _item["unique"] = False 
                            if "nullable" in item:
                                _item["nullable"] = item.get("nullable")
                            else:
                                _item["nullable"] = False 
                            _item["foreign"] = []
                            self.attributes[key] = _item
                    else:
                        _item["type"] = item
                        if "incremental" in item:
                            _item["incremental"] = item.get("incremental")
                        else:
                            _item["incremental"] = False 
                        if "unique" in item:
                            _item["unique"] = item.get("unique")
                        else:
                            _item["unique"] = False 
                        if "nullable" in item:
                            _item["nullable"] = item.get("nullable")
                        else:
                            _item["nullable"] = False 
                        _item["foreign"] = []
                        self.attributes[key] = _item
                """
                #i want to test this
                for key, item in _attributes.items():
                    _item = {}
                    
                    if isinstance(item, dict):
                        _item["type"] = item.get("type", "json")
                        _item["incremental"] = item.get("incremental", False)
                        _item["unique"] = item.get("unique", False)
                        _item["nullable"] = item.get("nullable", False)
                        _item["foreign"] = item.get("foreign", [])
                    else:
                        _item["type"] = item
                        _item["incremental"] = False
                        _item["unique"] = False
                        _item["nullable"] = False
                        _item["foreign"] = []

                    self.attributes[key] = _item
                #end of test

                return
            except json.JSONDecodeError:
                print("Invalid JSON. Please try again.")

    def __init__(self, module_name):

        modules_path = os.environ.get("PYLA_MODULES_PATH")

        self.module_name = module_name

        self.strip_module_name = str(module_name).replace(" ", "")
        self.slug_module_name = module_name.lower().replace(" ", "_")
        self.plural_strip_module_name = str(module_name).replace(" ", "") + 's'
        self.plural_slug_module_name = module_name.lower().replace(" ", "_") + 's'

        self.module_path = os.path.join(modules_path, self.strip_module_name)

        self.json_interpret()

        self.model_template = self.generate_model_template()
        self.controller_template = self.generate_controller_template()
        self.migration_template = self.generate_migration_template()
        self.route_template = self.generate_route_template()
        self.config_template = self.generate_config_template()
        self.service_provider_template = self.generate_service_provider_template()

        print(self.migration_template)
        
    def generate_controller_template(self) :
        extend_list = []
        header_list = [
            "App/Http/Controllers/Controller",
            f"App/Modules/{self.strip_module_name}/Models/{self.strip_module_name}",
            "Illuminate/Http/Request"
        ]

        for controller_header in self.controller_headers :
            append_if_not_exist(header_list, controller_header)

        for extend in self.controller_extends :
            append_if_not_exist(extend_list, extend)
            with open('config/extends.json') as file:
                data = json.load(file)
                headers = (data.get(extend))['headers']
                for header in headers :
                    append_if_not_exist(header_list, header)
        if(len(self.controller_extends) == 0):
            append_if_not_exist(extend_list, "Controller")

        _header = generate_headers(header_list)
        _extend = generate_extends(extend_list)
        
        def generate_controller_store_attributes():
            controller_attributes = ""
            for attribute in self.attributes:
                type = (self.attributes[attribute])["type"]

                if type in IMAGE_TYPE :
                    controller_attributes += f"""        
                // Avatar upload and save
                if ($request->hasFile('{attribute}')) {{
                    ${attribute} = $request->file('{attribute}');
                    $filename = time().'.'.${attribute}->getClientOriginalExtension();
                    $path = public_path('/uploads/images/');
                    ${attribute}->move($path, $filename);
                    $user->{attribute} = $filename;
                }}\n"""
                else :
                    controller_attributes += f"\t\t${self.slug_module_name}->{attribute} = $request->input('{attribute}');"
                
                controller_attributes += ";\n"
                
            return controller_attributes.strip()
        
        def generate_controller_update_attributes():
            controller_attributes = ""
            for attribute in self.attributes:
                type = (self.attributes[attribute])["type"]

                if type in IMAGE_TYPE :
                    controller_attributes += f""" 
                // Avatar upload and update
                if ($request->hasFile('{attribute}')) {{
                    ${attribute} = $request->file('{attribute}');
                    $filename = time().'.'.${attribute}->getClientOriginalExtension();
                    $path = public_path('/uploads/images/');
                    ${attribute}->move($path, $filename);

                    // Delete the previous {attribute} file, if it exists
                    if (!empty($user->{attribute})) {{
                        $previousImagePath = $path . $user->{attribute};
                        if (file_exists($previousImagePath)) {{
                            unlink($previousImagePath);
                        }}
                    }}

                    $user->{attribute} = $filename;
                }}\n"""
                else :
                    controller_attributes += f"\t\t${self.slug_module_name}->{attribute} = $request->input('{attribute}');"
                
                controller_attributes += ";\n"
                
            return controller_attributes.strip()
        
        _controller_store_attributes = generate_controller_store_attributes()
        _controller_update_attributes = generate_controller_update_attributes()


        """
        _class_code, _method_code, _part_code = interpret_blocks(controller_blocks)
        method = _part_code.get("method")
        _update_part = ""
        if(method == "update") :
            _update_part = _part_code.get("content")
            _controller_attributes_content += '\n\n\t\t' + _update_part + '\n'
        """
        
        _validations_content = ""
        if(self.controller_validators.items()):
            _validation_rules = "\n\t\t\t".join([
                f"{att} => '{key}',"
                for att,key in self.controller_validators.items()
            ])

            _validations_content = f"""
                $this->validate($request, [
                    {_validation_rules}
                ]);

                if ($validator->fails()) {{
                    return redirect()->back()->withErrors($validator)->withInput();
                }}\n"""
        
        controller_template = f"""
        <?php

        namespace App\Modules\{self.strip_module_name}\Controllers;

        {_header}

        class {self.strip_module_name}Controller extends {_extend}
        {{
            public function index()
            {{
                ${self.plural_slug_module_name} = {self.strip_module_name}::all();
                return view('{self.strip_module_name}::index', ['{self.plural_slug_module_name}' => ${self.plural_slug_module_name}]);
            }}

            public function show($id)
            {{
                ${self.slug_module_name} = {self.strip_module_name}::findOrFail($id);
                return view('{self.strip_module_name}::show', ['{self.slug_module_name}' => ${self.slug_module_name}]);
            }}

            public function create()
            {{
                return view('{self.strip_module_name}::create');
            }}

            public function store(Request $request)
            {{
            {_validations_content}
                ${self.slug_module_name} = new {self.strip_module_name}();
                {_controller_store_attributes}
                ${self.slug_module_name}->save();

                return redirect()->route('{self.slug_module_name}.index')->with('success', '{self.strip_module_name} created successfully!');
            }}

            public function edit($id)
            {{
                ${self.slug_module_name} = {self.strip_module_name}::findOrFail($id);
                return view('{self.strip_module_name}::edit',  ['{self.slug_module_name}' => ${self.slug_module_name}]);
            }}

            public function update(Request $request, $id)
            {{
            {_validations_content}
                ${self.slug_module_name} = {self.strip_module_name}::findOrFail($id);
                {_controller_update_attributes}
                ${self.slug_module_name}->save();

                return redirect()->route('{self.slug_module_name}.index')->with('success', '{self.strip_module_name} updated successfully!');
            }}

            public function destroy($id)
            {{
                ${self.slug_module_name} = {self.strip_module_name}::findOrFail($id);\t\n\t\t${self.slug_module_name}->delete();
                return redirect()->route('{self.slug_module_name}.index')->with('success', '{self.strip_module_name} deleted successfully!');
            }}
        }}"""

        return controller_template

    def generate_model_template(self) :

        extend_list = []
        header_list = ["Illuminate/Database/Eloquent/Model"]
        use_list = []



        for model_header in self.model_headers :
            append_if_not_exist(header_list, model_header)

        for extend in self.model_extends :
            append_if_not_exist(extend_list, extend)
            with open('config/extends.json') as file:
                data = json.load(file)
                headers = (data.get(extend))['headers']
                uses = (data.get(extend))['uses']
                for header in headers :
                    append_if_not_exist(header_list, header)
                for use in uses :
                    append_if_not_exist(use_list, use)
        if(len(self.model_extends) == 0):
            append_if_not_exist(extend_list, "Model")
        
        for use in self.model_uses :
            append_if_not_exist(use_list, use)
            with open('config/uses.json') as file:
                data = json.load(file)
                headers = (data.get(use))['headers']
                for header in headers :
                    append_if_not_exist(header_list, header)   

        _header = generate_headers(header_list)
        _extend = generate_extends(extend_list)
        _use = generate_uses(use_list)     
        
        def generate_model_functions():
            # Generate getAttribute() functions
            code = ""
            for fillable_attribute in self.fillables:
                attribute = self.attributes.get(fillable_attribute)
                type = attribute["type"]
                function_name = fillable_attribute.replace("_", " ").title().replace(" ", "")
                if(type in JSON_TYPE):
                    code += f"""
            public function get{function_name}()
            {{
                    $attribute = $this->getAttribute('{attribute}');
                    return json_decode($attribute, true) ?? [];
            }}"""
                else:
                    code += f"""
            public function get{function_name}()
            {{
                return $this->getAttribute('{attribute}');
            }}"""
                    
            if (self.attributes[fillable_attribute])["foreign"]:
                foreigns_key = (self.attributes[attribute])["foreign"]
                for foreign_key in foreigns_key :
                    code += f"""
                // Define any additional relationships here
                public function customer()
                {{
                     return $this->belongsTo(Customer::class);
                 }}"""
            return code

        _fillable_attributes_content = "[{}];".format(",".join(["'{}'".format(attr) for attr in self.fillables]))
        _guarded_attributes_content = "[{}];".format(",".join(["'{}'".format(attr) for attr in self.guardeds]))
        _hidden_attributes_content = "[{}];".format(",".join(["'{}'".format(attr) for attr in self.hiddens])) 
        _visible_attributes_content = "[{}];".format(",".join(["'{}'".format(attr) for attr in self.visibles]))

        _attribute_functions = generate_model_functions()
        slug_module_name = self.slug_module_name

        model_template = f"""
        <?php
        namespace App\Modules\{slug_module_name}\Models;
        {_header}
        class {slug_module_name} extends {_extend}
        {{
            {_use}
            //protected $table = '{self.slug_module_name}_table';
            //protected $connection = 'mysql';
            //protected $primaryKey = 'id';
            //protected $keyType = 'int';
            //public $incrementing = true;
            //public $timestamps = true;
            //protected $dateFormat = 'Y-m-d H:i:s';
            //protected $casts = ['is_admin' => 'boolean', 'settings' => 'json'];

            protected $fillable = {_fillable_attributes_content}

            protected $guarded = {_guarded_attributes_content}

            protected $hidden = {_hidden_attributes_content}
            
            protected $visible = {_visible_attributes_content}

            {_attribute_functions}
        }}"""    
        
        return model_template 

    def generate_migration_template(self):
        
        extend_list = []
        header_list = [
            "Illuminate/Database/Migrations/Migration",
            "Illuminate/Database/Schema/Blueprint",
            "Illuminate/Support/Facades/Schema"
        ]


        for migration_header in self.migration_headers :
            append_if_not_exist(header_list, migration_header)

        for extend in self.migration_extends :
            append_if_not_exist(extend_list, extend)
            with open('config/extends.json') as file:
                data = json.load(file)
                headers = (data.get(extend))['headers']
                for header in headers :
                    append_if_not_exist(header_list, header)
        if(len(self.migration_extends) == 0):
            append_if_not_exist(extend_list, "Migration")

        _header = generate_headers(header_list)
        _extend = generate_extends(extend_list)

        def generate_migration_attributes():
            migration_attributes = ""
            for attribute in self.attributes:
                type = (self.attributes[attribute])["type"]

                if type in JSON_TYPE :
                    migration_attributes += f"\t\t\t$table->json('{attribute}'"
                elif type in IMAGE_TYPE :
                    migration_attributes += f"\t\t\t$table->string('{attribute}'"
                else :
                    migration_attributes += f"\t\t\t$table->{type}('{attribute}'"

                if type == 'decimal':
                    migration_attributes += f",10,2"
                    
                migration_attributes += ")"

                if((self.attributes[attribute])["nullable"]):
                    migration_attributes += '->nullable()'

                if((self.attributes[attribute])["unique"]):
                    migration_attributes += '->unique()'

                if (self.attributes[attribute])["foreign"]:
                    foreigns_key = (self.attributes[attribute])["foreign"]
                    migration_attributes += generate_migration_foreign_lines_code(attribute, foreigns_key)
                
                migration_attributes += ";\n"

            if(self.migration.get('remembertoken')):
                migration_attributes += "\t\t$table->rememberToken();"

                
            return migration_attributes.strip()

        migration_attributes = generate_migration_attributes()


        migration_template = f"""
        <?php

        {_header}
        class Create{self.plural_strip_module_name}Table extends {_extend}
        {{
            public function up()
            {{
                Schema::create('{self.plural_slug_module_name}', function (Blueprint $table) {{
                    {migration_attributes}
                    $table->timestamps();
                }});
            }}

            /**
            * Reverse the migrations.
            *
            * @return void
            */
            public function down()
            {{
                Schema::dropIfExists('{self.plural_slug_module_name}');
            }}
        }}
        """

        return migration_template

    def generate_route_template(self):
        
        route_template = f"""
        <?php

        use App\Modules\{self.strip_module_name}\Controllers\{self.strip_module_name}Controller;

        // routes/web.php
        Route::get('/{self.strip_module_name}', '{self.strip_module_name}Controller@index')->name('{self.slug_module_name}.index');
        Route::get('/{self.strip_module_name}/{{id}}', '{self.strip_module_name}Controller@show')->name('{self.slug_module_name}.show');
        Route::get('/{self.strip_module_name}/create', '{self.strip_module_name}Controller@create')->name('{self.slug_module_name}.create');
        Route::post('/{self.strip_module_name}', '{self.strip_module_name}Controller@store')->name('{self.slug_module_name}.store');
        Route::get('/{self.strip_module_name}/{{id}}/edit', '{self.strip_module_name}Controller@edit')->name('{self.slug_module_name}.edit');
        Route::put('/{self.strip_module_name}/{{id}}', '{self.strip_module_name}Controller@update')->name('{self.slug_module_name}.update');
        Route::delete('/{self.strip_module_name}/{{id}}', '{self.strip_module_name}Controller@destroy')->name('{self.slug_module_name}.destroy');

        """

        return route_template

    def generate_config_template(self):
        
        config_template = f"""
        <?php

        return [
            // 'your_module_setting' => 'your_value',
            // 'another_module_setting' => 'another_value',
            // Add more configuration options here
            // to read config value use $value = config('your_module_setting');
        ];

        """

        return config_template

    def generate_service_provider_template(self):
        
        service_provider_template = f"""
        <?php

        namespace App\Modules\{self.strip_module_name};

        use Illuminate\Support\ServiceProvider;

        class {self.strip_module_name}ServiceProvider extends ServiceProvider
        {{
            /**
            * Register services.
            *
            * @return void
            */
            public function register()
            {{
                // Register any module-specific services or bindings here
            }}

            /**
            * Bootstrap services.
            *
            * @return void
            */
            public function boot()
            {{
                // Load module routes
                $this->loadRoutesFrom(__DIR__.'/Routes/web.php');

                // Load module views
                $this->loadViewsFrom(__DIR__.'/Views', '{self.slug_module_name}');

                // Load module migrations
                $this->loadMigrationsFrom(__DIR__.'/Migrations');

                // Merge the module configuration
                $this->mergeConfigFrom(__DIR__.'/config/config.php', '{self.slug_module_name}');
                // if you want to read config use $configValue = config('{self.slug_module_name}.setting');

                // Publish the module configuration file
                $this->publishes([
                    __DIR__.'/config/config.php' => config_path('{self.slug_module_name}.php'),
                ], 'config');
                /**
                In this example, we are using the $this->publishes method to define a publishing rule for a configuration file within the UserManager module. 
                This rule specifies that when users of the module run the php artisan vendor:publish command, 
                the specified configuration file should be copied from the module's directory to the application's config directory.

                Here's a breakdown of the code:

                __DIR__.'/config/config.php' represents the source path of the configuration file. 
                This path assumes that the config.php file for the UserManager module is located within the config directory of the module.

                config_path('user-manager.php') represents the destination path where the configuration file will be published within the application. 
                config_path() is a Laravel helper function that returns the full path to the config directory of the application. By specifying 'user-manager.php' as the filename, 
                we indicate that the published configuration file should be named user-manager.php.

                'config' is the optional group name for the publishing rule. 
                It is used to categorize or group different sets of published files. In this case, the rule is categorized under the 'config' group.

                When users run the php artisan vendor:publish command and select the 'config' group (by using the --tag=config option), 
                the specified configuration file will be copied to the application's config directory, allowing users to customize the configuration for the UserManager module.

                It's important to note that the publishing rule defined using $this->publishes provides flexibility for module users to customize the published files 
                without modifying the original files within the module.
                */

                // Publish module assets
                $this->publishes([
                    __DIR__.'/Assets' => public_path('{self.slug_module_name}'), 
                ], 'public');

                /**
                In this example, we are using the $this->publishes method to define a publishing rule for the assets directory within the UserManager module. 
                This rule specifies that when users of the module run the php artisan vendor:publish command, 
                the specified assets directory should be copied from the module's directory to the application's public/user-manager directory.

                Here's a breakdown of the code:

                __DIR__.'/Assets' represents the source directory of the assets. This path assumes that the assets directory is located within the module's directory structure.

                public_path('user-manager') represents the destination path where the assets directory will be published within the application. 
                public_path() is a Laravel helper function that returns the full path to the public directory of the application. By specifying 'user-manager' as the subdirectory, 
                we indicate that the published assets should be placed in the public/user-manager directory.

                'public' is the optional group name for the publishing rule. It is used to categorize or group different sets of published files. 
                In this case, the rule is categorized under the 'public' group.

                When users run the php artisan vendor:publish command and select the 'public' group (by using the --tag=public option), 
                the specified assets directory will be copied to the application's public/user-manager directory. 
                This allows users to access the module's assets directly from the public directory, making them available to the web browser.

                It's important to note that the publishing rule defined using $this->publishes provides a way for module users to publish the module's assets to the appropriate public directory, 
                making them accessible to the web server. This separation of assets from the module's source code ensures that the assets can be safely served by the web server without exposing
                  any sensitive module files.
                */
            }}
        }}

        // Remember to register the YourModuleNameServiceProvider within the config/app.php file of your Laravel application by adding it to the providers array.
        /**
        'providers' => [
            // Other service providers...
            App\Modules\YourModuleName\YourModuleNameServiceProvider::class,
        ],
        */
        // This will ensure that your module's service provider is loaded by Laravel and its functionality is available within your application.

        """

        return service_provider_template

    #def generate_index_view_template() :
    #def generate_create_view_template() :
    #def generate_edit_view_template() : 
    #def generate_show_view_template() :
    #def generate_delete_view_template() :
    #def generate_form_view_template() :
    #def generate_partial_view_template() :
    #def generate_modal_view_template() :
    #def generate_error_view_template() :  

