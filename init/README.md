# Level0

Python言語においてパッケージとはディレクトリ、モジュールとはPythonのスクリプトファイルのことです。

そのため、極端な話しとして、Pythonスクリプトファイルがどこかディレクトリに格納されていればそれはパッケージです。

例えば、`package0`というデイレクトリに、`my_module.py`というPythonスクリプトファイルがあり、その中に`my_array`や`my_func`といったPythonオブジェクトが記述されていたとします。

```
package0
└── my_module.py
```

この場合、以下のようなコードを実行することで、`my_array`や`my_func`が直ちに参照可能となります。

## import パッケージ名.モジュール名

```py
>>> import package0.my_module
>>> package0.my_module.my_array
array(['1', '2', '3'], dtype='<U1')
>>> package0.my_module.my_func(package0.my_module.my_array)
array([1, 2, 3])
```

この書き方は、`as`でより簡略化できます。

```py
>>> import package0.my_module as mod
>>> mod.my_array
array(['1', '2', '3'], dtype='<U1')
>>> mod.my_func(mod.my_array)
array([1, 2, 3])
```

## from パッケージ名.モジュール名 import オブジェクト名

オブジェクトそのものを`import`してくることも可能です。

各々`import`したり、

```py
>>> from package0.my_module import my_array
>>> from package0.my_module import my_func
```

`,`で同時に`import`したり、

```py
>>> from package0.my_module import my_array, my_func
```

ワイルドカード（*）で、そのモジュールにある全てのオブジェクトを`import`する書き方があります。

```py
>>> from package0.my_module import *
```

ただし、別のモジュールにある同名のオブジェクトを後から定義した場合、上書きされてしまうことには注意が必要です。

# Level1（\_\_init\_\_.py/__all__の利用）

一般にPythonパッケージでは、各ディレクトリごとに`__init__.py`というファイルが配置されます。

このファイルの目的は以下の通りです。

- *そのディレクトリをパッケージと認識するため*
  - （ただしPython 3.3以降必須ではないが、昔からの慣習として空の`__init__.py`を配置することが多い）
  - 昔はこういうエラーが出ていたらしい（by ChatGPT 3.5）
  ```
  ImportError: No module named 'mypackage'
  ```
- *初期化*
  - そのパッケージの`import`時に、最初に実行されるコードをここに書きます
  - 例1: そのパッケージのバージョンを示すメッセージ
  - 例2: 他のオブジェクトが共通して使うようなオブジェクト
- *インポートの管理*
  - あるモジュール内で、別のモジュールやオブジェクトを`import`していた場合、そのモジュールの`import`時に、それらまでついでに呼び出されてしまいます
  - これを防ぐためには`__all__`という特殊変数を`__init__.py`、もしくはモジュール内部に記入します

ここでは、先ほどのpackage0をコピーしてpackage1とした上で、以下のように`__init__.py`をpackage1以下に配置し、

```
package1
├── __init__.py
└── my_module.py
```

`__init__.py`に`from .my_module import *`、`my_module.py`に`__all__ = ['my_array', 'my_func']`という追記を行いました。

これにより、package0では以下のように`np`まで`import`されていましたが、

```py
>>> from package0.my_module import *
>>> dir()
['__annotations__', '__builtins__', '__doc__', '__loader__', '__name__', '__package__', '__spec__', 'my_array', 'my_func', 'np']
```

package1では、

```py
>>> from package1.my_module import *
>>> dir()
['__annotations__', '__builtins__', '__doc__', '__loader__', '__name__', '__package__', '__spec__', 'my_array', 'my_func']
```

のように、余計なモジュールをユーザーが参照せずに済みます。

# Level2（サブパッケージと\_\_init\_\_.py）

パッケージの中に入れ子でパッケージを作ることもできます（サブパッケージという）。

例えば[scikit-learn](https://github.com/scikit-learn/scikit-learn/tree/main/sklearn)のGitHubを参照すると、`sklearn`以下に、`cluster`や`svm`といったサブパッケージが配置されているのがわかります。

この場合も、Level1の時と同様に、各ディレクトリごとに`__init__.py`が配置されます。

```
package2
├── __init__.py
├── my_module.py
├── subpackage1
│   ├── __init__.py
│   └── my_module.py
└── subpackage2
    ├── __init__.py
    ├── my_module.py
    └── subpackage3
        ├── __init__.py
        └── my_module.py
```

サブパッケージ以下にあるモジュールを参照する場合は、以下のように書きます（上書きを避けるため、ここでは*import パッケージ名.モジュール名*の書き方を利用）。

```py
>>> import package2.my_module as mod1
>>> import package2.subpackage1.my_module as mod2
>>> import package2.subpackage2.my_module as mod3
>>> import package2.subpackage2.subpackage3.my_module as mod4

>>> mod1.my_array
array(['1', '2', '3'], dtype='<U1')
>>> mod2.my_array
array(['1', '2', '3'], dtype='<U1')
>>> mod3.my_array
array(['1', '2', '3'], dtype='<U1')
>>> mod4.my_array
array(['1', '2', '3'], dtype='<U1')

>>> mod1.my_func(mod1.my_array)
array([1, 2, 3])
>>> mod2.my_func(mod2.my_array)
array([1, 2, 3])
>>> mod3.my_func(mod3.my_array)
array([1, 2, 3])
>>> mod4.my_func(mod4.my_array)
array([1, 2, 3])
```