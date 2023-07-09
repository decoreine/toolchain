import json

def append_if_not_exist(my_list, item):
    if item not in my_list:
        my_list.append(item)

def get_first_level_keys(dictionary):
    return list(dictionary.keys())

def get_first_level_values(dictionary):
    return list(dictionary.values())
    
def get_json_dictionary(json_path):
    with open(json_path) as file:
        dictionary = json.load(file)
    return dictionary

def get_json_value_by_key(dictionary, key):
    if key in dictionary:
        return dictionary.get(key)
    else:
        return None


def get_json_string(json_path):
    with open(json_path) as file:
        dictionary = json.load(file)
        json_string = json.dumps(dictionary)
    return json_string

def get_json_string_value_by_key(dictionary, key):
    if key in dictionary:
        dict = dictionary.get(key)
        json_string = json.dumps(dict)
        return json_string
    else:
        return None