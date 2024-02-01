from .my_module import *

import inspect

print('__init__.py in package1 is loaded...\n')
print(f'I could find my_array ({my_array}) and my_func ({inspect.getsource(my_func)})')