import sys
import os

folder_path = __file__.split(os.sep)[:-3]
folder_path.append('sdk')
sys.path.insert(0, os.sep.join(folder_path))
