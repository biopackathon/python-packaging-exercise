import numpy as np

# 定数（Numpy配列）
my_array = np.array(["1", "2", "3"])


# 関数
def my_func(x):
    return x.astype(np.int64)


__all__ = ["my_array", "my_func"]
