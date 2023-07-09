import os
import shutil
import json
import fileinput

def add_provider_to_config(provider_class, config_path):
    # Open the config/app.php file in read mode
    with fileinput.FileInput(config_path, inplace=True) as file:
        # Iterate over each line in the file
        for line in file:
            # Check if the line contains the 'providers' array definition
            if "'providers' => [" in line:
                # Print the line as it is
                print(line, end='')

                # Add the provider class to the 'providers' array
                print(f"        {provider_class},", end='\n')
            else:
                # Print the line as it is
                print(line, end='')

def integrate_module(module_name, laravel_project_path, module_namespace_prefix):
    # Move module directory to app/Modules in Laravel project
    module_path = f"app/Modules/{module_name}"
    laravel_module_path = os.path.join(laravel_project_path, "app", "Modules", module_name)
    shutil.move(module_path, laravel_module_path)

    # Update composer.json file with module's namespace
    composer_file = os.path.join(laravel_project_path, "composer.json")
    with open(composer_file, "r+") as file:
        composer_data = json.load(file)
        composer_data["autoload"]["psr-4"][f"{module_namespace_prefix}\\{module_name}\\"] = f"app/Modules/{module_name}/"
        file.seek(0)
        json.dump(composer_data, file, indent=4)
        file.truncate()

    # Run composer dump-autoload
    os.system("composer dump-autoload")

    # Create the module's service provider
    service_provider_name = f"{module_name}ServiceProvider"
    os.system(f"php artisan make:provider {service_provider_name}")

    # Register the module's routes, views, and other components in the service provider
    service_provider_path = os.path.join(laravel_project_path, "app", "Providers", f"{service_provider_name}.php")
    with open(service_provider_path, "r") as file:
        service_provider_content = file.read()
        service_provider_content = service_provider_content.replace(
            "use Illuminate\Support\ServiceProvider;", 
            "use Illuminate\Support\ServiceProvider;\nuse Illuminate\Routing\Router;")
        service_provider_content = service_provider_content.replace(
            "public function register()", 
            f"public function register()\n    {{\n        $this->app->register(RouteServiceProvider::class);\n\n        $router = $this->app['router'];\n        $router->middlewareGroup('web', [StartSession::class, VerifyCsrfToken::class]);\n        $router->middlewareGroup('api', [throttle:60,1]);\n        $router->middlewareGroup('api.auth', [\Illuminate\Auth\Middleware\Authenticate::class]);\n        $router->middlewareGroup('api.guest', [\Illuminate\Auth\Middleware\EnsureGuest::class]);\n        $router->middlewareGroup('api.limit', [\App\Http\Middleware\ApiRequestsLimit::class]);\n\n        $router->group([\n            'middleware' => 'web',\n            'prefix' => '{module_name.lower().replace(' ', '_')}'\n        ], function ($router) {{\n            require __DIR__ . '/routes/web.php';\n        }});\n    }}")
    with open(service_provider_path, "w") as file:
        file.write(service_provider_content)

    # Register the module's service provider in config/app.php
    config_app_file = os.path.join(laravel_project_path, "config", "app.php")
    with open(config_app_file, "r") as file:
        config_app_content = file.read()
        config_app_content = config_app_content.replace(
            "'providers' => [", 
            f"'providers' => [\n        // ...\n        {module_namespace_prefix}\\{module_name}\\{service_provider_name}::class,")
    with open(config_app_file, "w") as file:
        file.write(config_app_content)

    print(f"Module '{module_name}' integrated successfully!")

if __name__ == "__main__":
    module_name = input("Enter the module name: ")
    integrate_module(module_name)