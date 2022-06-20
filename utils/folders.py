import os
from data.config import *

import os
from data.config import *

def tasks_sheet_creator(directory, tasks_sheet=[]):
    for file in os.listdir(directory):
        if os.path.isfile(rf'{directory}{file}'):
            tasks_sheet.append(file)
        if os.path.isdir(rf'{directory}{file}'):
            tasks_sheet_creator(directory=rf'{directory}{file}', tasks_sheet=tasks_sheet)


files = os.listdir(tasks_path)

print(files[1])

