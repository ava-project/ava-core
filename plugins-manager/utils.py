import os, shutil

# Handler for retrieving plugins names and files' extension
# @params:
#   - path: string  (/path/to/the/plugins/directory)
#   - skip: string  (extension to skip i.e "json")
#   - dictionary: the dictionary to fill.
#
# @behave: raise an error if the specified directory does not exist.
def retrieve_plugins_name_and_files_extension(path, skip, dictionary):
    if os.path.isdir(path) == False:
        raise
    for directory in os.listdir(path):
        for files in os.listdir(path + '/' + directory):
            if files.find(".") > 0 and files[files.find(".") + 1:] != skip:
                dictionary[directory] = files[files.find(".") + 1:]

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
