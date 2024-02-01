import numpy as np
from mypackageabc.my_module import my_array, my_func

def test_my_func_type():
    assert callable(my_func)

def test_my_func_value():
    values = my_func(my_array)
    for element in values:
        assert type(element) == np.int64