import os

def retrieve_plugins_name_and_files_extension(path, skip, dictionary):
    for directory in os.listdir(path):
        for files in os.listdir(path + '/' + directory):
            if files[files.find(".") + 1:] == skip:
                continue
            dictionary[directory] = files[files.find(".") + 1:]
