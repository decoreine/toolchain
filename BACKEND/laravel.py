'''
How to Remove Public From URL in Laravel

solution 1 : in the first you have to move index.php from public to root and change all link and replace /../somethink by /somethink
solution 2 : Update the code into your .htaccess file:
               <IfModule mod_rewrite.c>
                  RewriteEngine On 
                  RewriteRule ^(.*)$ public/$1 [L]
               </IfModule>
'''

from lib.moduless import *
from lib.modules import *
from lib.module import *
from lib.config import *
from lib.create import *
from lib.build import *

1
class Setup :
    def __init__(self):
        #read packege configuration
        Config()
        #create json template for all modules
        Create()
        #build php classes from json template for all modules
        Build()

if __name__ == "__main__":
#    module_names = input("Enter the names of the modules (separated by commas): ").split(",")

#    for module_name in module_names:
#        module_name = module_name.strip().replace('"', '')
#        moduless = Moduless()
#        moduless.create_module(module_name)

    setup = Setup()


"""
collect all function and attrebute for module in one calss and use the result in creation of model controller attrebute ...
create json templating for view and create function intrpret json and relate each view with json templating
create functions to create view model and migration from attributes
create function for provider
create vue view with javascript to creat modal for add or delete
create function to stocke model of module in folder of models
create function to add module route to menues configuration
let programe accept the huge json project  with all attrebute fillable hiden and ...
create chortkut to use it after to make modefecation or add yo the module like add lines or add controller or views
if there is sub json in principal json we have to stocke sub json as is it but we crete automatic function to extract the data from sub json and we do the same think for sub sub json
create principle view type like table or datat display (for both laravel or vue.js)
crete uml app to build json from uml and create uml block to crete json for plusior class in one file or keep on uml to crete on json

create layout library
create chart library
create datatable library


light tree
----------
└── app
    └── Modules
        └── YourModuleName
            ├── Controllers
            │   └── YourController.php ok
            ├── Models
            │   └── YourModel.php ok
            ├── Views
            │   └── your-view.blade.php
            ├── Migrations
            │   └── yyyy_mm_dd_hhmmss_create_your_table.php ok
            ├── Routes
            │   └── web.php ok
            ├── Config
            │   └── config.php ok
            └── YourModuleNameServiceProvider.php ok

complete tree
-------------
- app
  |- Modules
     |- ModuleName
        |- Console
        |- Http
           |- Controllers
              |- ModuleController.php ok
           |- Middleware
              |- CustomMiddleware.php
           |- Requests
              |- StoreModuleRequest.php
              |- UpdateModuleRequest.php
           |- routes
              |- web.php ok
        |- Models
           |- Module.php ok
        |- Database
           |- Migrations
              |- 2023_06_01_000000_create_module_table.php ok
        |- Resources
           |- Views
              |- index.blade.php
              |- detail.blade.php
           |- Lang
              |- en
                 |- module.php
        |- Providers
           |- ModuleServiceProvider.php
        |- Tests
        |- composer.json
"""
