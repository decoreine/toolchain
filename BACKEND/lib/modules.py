import fileinput

def generate_headers(header_list) :
    headers = "\n"  
    for header in header_list :
        _header = header.replace('/','\\')
        _header = f"\tuse {_header};\n"
        headers += _header;
    return headers

def generate_extends(extend_list) :  
    extends = "" 
    i=0 
    for extend in extend_list :
        i += 1
        extends += extend;
        if(i == len(extend_list)):
            extends += ""
        else :
            _extends += ","
    return extends

def generate_uses(use_list) :  
    _uses = "\n\t\tuse " 
    i=0 
    for use in use_list :
        i += 1
        _uses += use;
        if(i == len(use_list)):
            _uses += ";"
        else :
            _uses += ","
    return _uses

def generate_migration_foreign_lines_code(column_name, foreign_keys):
    migration_code = ""

    for foreign_key in foreign_keys:
        table_name = foreign_key['table']
        key_name = foreign_key['key']
        on_delete = foreign_key['on_delete']
        on_update = foreign_key['on_update']
        foreign_type = foreign_key['type']

        if foreign_type == 'belongsTo':
            migration_code += "\n\t\t\t$table->foreign('{column}')->references('{key}')->on('{table}')->onDelete('{on_delete}')->onUpdate('{on_update}');".format(
                column=column_name,
                key=key_name,
                table=table_name,
                on_delete=on_delete,
                on_update=on_update
            )
        elif foreign_type == 'hasOne':
            migration_code += "\n\t\t\t$table->foreign('{column}')->references('{key}')->on('{table}')->onDelete('{on_delete}')->onUpdate('{on_update}');".format(
                column=column_name,
                key=key_name,
                table=table_name,
                on_delete=on_delete,
                on_update=on_update
            )
        elif foreign_type == 'hasMany':
            migration_code += "\n\t\t\t$table->foreign('{column}')->references('{key}')->on('{table}')->onDelete('{on_delete}')->onUpdate('{on_update}');".format(
                column=column_name,
                key=key_name,
                table=table_name,
                on_delete=on_delete,
                on_update=on_update
            )
        elif foreign_type == 'belongsToMany':
            pivot_table = foreign_key['pivot_table']
            migration_code += "\n\t\t\t$table->foreign('{column}')->references('{key}')->on('{table}')->onDelete('{on_delete}')->onUpdate('{on_update}');".format(
                column=column_name,
                key=key_name,
                table=table_name,
                on_delete=on_delete,
                on_update=on_update
            )
            migration_code += "\n\t\t\t$table->foreign('{key}')->references('{column}')->on('{pivot_table}')->onDelete('{on_delete}')->onUpdate('{on_update}');".format(
                column=column_name,
                key=key_name,
                pivot_table=pivot_table,
                on_delete=on_delete,
                on_update=on_update
            )
        elif foreign_type == 'hasOneThrough':
            through_table = foreign_key['through_table']
            first_key = foreign_key['first_key']
            second_key = foreign_key['second_key']
            migration_code += "\n\t\t\t$table->foreign('{column}')->references('{key}')->on('{through_table}')->onDelete('{on_delete}')->onUpdate('{on_update}');".format(
                column=column_name,
                key=key_name,
                through_table=through_table,
                on_delete=on_delete,
                on_update=on_update
            )
        elif foreign_type == 'hasManyThrough':
            through_table = foreign_key['through_table']
            first_key = foreign_key['first_key']
            second_key = foreign_key['second_key']
            migration_code += "\n\t\t\t$table->foreign('{column}')->references('{key}')->on('{through_table}')->onDelete('{on_delete}')->onUpdate('{on_update}');".format(
                column=column_name,
                key=key_name,
                through_table=through_table,
                on_delete=on_delete,
                on_update=on_update
            )

    return migration_code

def generate_model_foreign_functions(attributes):
    functions = []

    for attribute, attribute_details in attributes.items():
        function_name = attribute
        if '_' in attribute:
            function_name = attribute.split('_')[0]

        foreign_keys = attribute_details['foreign']
        for foreign_key in foreign_keys:
            foreign_type = foreign_key['type']
            table_name = foreign_key['table']
            key_name = foreign_key['key']
            on_delete = foreign_key['on_delete']
            on_update = foreign_key['on_update']

            function = f"""    /**
     * Get the {attribute} associated with the {table_name}.
     */
    public function {function_name}()
    {{
        """

            if foreign_type == 'belongsTo':
                function += f"return $this->{function_name}()->belongsTo({table_name}::class, '{key_name}');"
            elif foreign_type == 'hasOne':
                function += f"return $this->{function_name}()->hasOne({table_name}::class, '{key_name}');"
            elif foreign_type == 'hasMany':
                function += f"return $this->{function_name}()->hasMany({table_name}::class, '{key_name}');"
            elif foreign_type == 'belongsToMany':
                pivot_table = foreign_key['pivot_table']
                function += f"return $this->{function_name}()->belongsToMany({table_name}::class, '{pivot_table}', 'user_id', 'role_id');"
            elif foreign_type == 'hasOneThrough':
                through_table = foreign_key['through_table']
                first_key = foreign_key['first_key']
                second_key = foreign_key['second_key']
                function += f"return $this->{function_name}()->hasOneThrough({table_name}::class, '{through_table}', '{first_key}', '{second_key}');"
            elif foreign_type == 'hasManyThrough':
                through_table = foreign_key['through_table']
                first_key = foreign_key['first_key']
                second_key = foreign_key['second_key']
                function += f"return $this->{function_name}()->hasManyThrough({table_name}::class, '{through_table}', '{first_key}', '{second_key}');"

            function += "\n    }"
            functions.append(function)

    return functions

def generate_migration_foreign_line_code_old(column_name, foreign_key):
    table_name = foreign_key['table']
    key_name = foreign_key['key']
    on_delete = foreign_key['on_delete']
    on_update = foreign_key['on_update']
    
    migration_code = "\n\t\t\t$table->foreign('{column}')->references('{key}')->on('{table}')->onDelete('{on_delete}')->onUpdate('{on_update}')".format(
        column=column_name,
        key=key_name,
        table=table_name,
        on_delete=on_delete,
        on_update=on_update
    )
    
    return migration_code

def generate_model_foreign_functions_old(attributes):
    functions = []
    for attribute in attributes:
        function_name = attribute
        if '_' in attribute :
            function_name = attribute.split('_')[0]
        function = f"""    /**
     * Get the {attribute} associated with the order.
     */
    public function {function_name}()
    {{
        return $this->belongsTo({function_name.capitalize()}::class);
    }}"""
        functions.append(function)
    return functions
