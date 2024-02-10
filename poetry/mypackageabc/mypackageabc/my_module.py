import numpy as np

# Creates a NumPy array from the given string elements
my_array = np.array(["1", "2", "3"])

def my_func(x):
    """Converts a Numpy array with string elements into an integer Numpy array.

    Args:
        A Numpy array with string elements (e.g., my_array)

    Returns:
        A Numpy array with int64 elements

    Example:
        >>> import mypackageabc as my
        >>> my.my_func(my.my_array)

    Note:
        This is very simple function only for the demonstration

    """
    return x.astype(np.int64)


__all__ = ["my_array", "my_func"]
