import numpy as np
from mypackageabc.my_module import my_array, my_func

def test_my_array_type():
    assert type(my_array) == np.ndarray

def test_my_array_value():
    for element in my_array:
        assert isinstance(element, str)

