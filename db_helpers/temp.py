from datetime import timedelta,datetime
import os
from pathlib import Path
d = datetime.date(datetime.today())
d2 = d + timedelta(days=1)
directory = 'csv_archives'
parent_directory = Path().absolute()
dir_path = os.path.join(parent_directory, directory)
try:
    os.mkdir(dir_path)
except FileExistsError as e:
    pass
new_file_path = os.path.join(dir_path, str(d))


x = 'Sembawang,Kok,ME2,P,,P,'
print(x.split(','))
# print("File      Path:", Path(__file__).absolute())
# print("Directory Path:", Path().absolute())
# print ("Is it Directory?" + str(path.isdir('csv_archives')))
