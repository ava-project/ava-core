import os, shutil, json

# Format the output.
def format_output(*args):
    result = "["
    for arg in args:
        result += str(arg)
        result += str(":")
    result = result[:-1] + str("]: ")
    return result


# Handler for removing a directory and all its content
# @param:
#   - path: string (/path/to/the/directory/to/remove)
#
# @behave: raise an error if the specified directory does not exist.
def remove_directory(path):
    if os.path.isdir(path) == True:
        shutil.rmtree(path)
    else:
        raise

# Parse a json file and store key and value into the given dictionary.
# @params:
#   - path: string (/path/to/the/directory/containing/the/json/file)
#   - dictionary: the dictionary to fill with data.
#
# @behave: display an error message in case of invalid path to directory containing a json file.
def parse_json_file_to_dictionary(path, dictionary):
    if os.path.isdir(path) == True:
        for file in os.listdir(path):
            if file.find(".json") > 0:
                with open(path + '/' + file) as json_file:
                    data = json.load(json_file)
                for key, value in data.items():
                    dictionary[key] = value
    else:
        print(format_output(__name__, parse_json_file_to_dictionary.__name__) + "error invalid path")
