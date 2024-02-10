# setuptools_twine

ここでは`setuptools`や、`twine`といったツールを利用したPythonパッケージ開発を行います。

# 1. 仮想環境構築

ここでは`conda`コマンドを使って、仮想環境を構築していきます。

```shell
# 仮想環境構築
conda create -n packaging python=3.12 -y
# 作成した仮想環境に切り替え
conda activate packaging
# 必要なパッケージのインストール
conda install numpy -y # 関数の実装
conda install pytest -y # テスト
conda install pytest-cov -y # テスト
conda install sphinx -y # ドキュメント
conda install flake8 -y # Linter
conda install black -y # Formatter
conda install twine -y # パッケージの公開
# インストールしたライブラリの一覧
conda list
# 仮想環境の一覧
conda env list
# base環境に戻る
conda deactivate
```

# 2. ディレクトリ構成
最終的に以下のようなディレクトリ構成にしていきます。

```shell
.
├── LICENSE                   <- OSSライセンス
├── README.md                 <- 今読んでいるこのファイル
├── build                     <- ビルド時に生成される
│   ├── bdist.macosx-11.0-arm64
│   └── lib
│       └── mypackageabc
│           ├── __init__.py
│           └── my_module.py
├── dist                      <- ビルド時に生成される
│   ├── mypackageabc-0.99.0-py3-none-any.whl
│   └── mypackageabc-0.99.0.tar.gz
├── mypackageabc                 <- パッケージの本体
│   ├── __init__.py
│   └── my_module.py
├── mypackageabc.egg-info        <- ビルド時に生成される
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── dependency_links.txt
│   ├── requires.txt
│   └── top_level.txt
├── setup.cfg                 <- setup.pyのメタデータ
├── setup.py                  <- 重要な設定ファイル
└── tests                     <- pytest用のテストコード
    ├── __init__.py
    ├── test_my_array.py
    └── test_my_func.py
```

なお[cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage)など、必要なディレクトリ、ファイルを自動生成してくれるツールもありますが、出力されるディレクトリ、ファイルが多く、やや過剰なように感じたので、ここでは1つ1つボトムアップにこれらディレクトリ、ファイルを用意していきます。

## 2.1. パッケージ、モジュール

ここでは、パッケージ名を`mypackageabc`として、同名のディレクトリを切り、その中に`my_module.py`を作成します。

```py
# my_module.py
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
```

なお`"""`で挟んだブロック記法はDocstringという関数のドキュメントを生成する仕組みに関係しており、このように書くことで、パッケージロード後`help(関数名)`とすることで、この説明文が画面に出力されるようになります。

DocstringにはReStructuredTextスタイル、Numpyスタイル、Googleスタイルなどありますが、今回はGoogleスタイルを採用しました。

以下のように`__init__.py`も設置しておきます。

```py
# __init__.py
from .my_module import *
```

ここでは扱いませんが、Sphinxというツールを使うことで、このDocstringの行が抽出され、よりユーザーが読みやすいHTMLページを作成できます。

## 2.2. LICENSE
どのようなOSSライセンスを設定すべきなのかは[OSSライセンスのまとめ @ Bio”Pack”athon2023#7](https://www.youtube.com/watch?v=P9NJnylvMcc)などをご確認ください。

ここでは、[MIT LICENSE](https://opensource.org/license/mit/)の原文をコピペして、`<YEAR><COPYRIGHT HOLDER>`の箇所だけ書き換えます。

## 2.3. setup.py

以下のように書くだけです。

後ほどパッケージのビルド時に、このスクリプトが実行されます。

```py
# setup.py
from setuptools import setup
setup()
```

## 2.4. setup.cfg

`setup`関数の引数を、設定ファイルとして書いたものです。

以下のように書きました。

```py
# setup.cfg
[metadata]
name = mypackageabc
version = 0.99.0
description = My package description
long_description = My package is great!!!!!!
long_description_content_type = text/x-rst
author = Koki Tsuyuzaki
author_email = k.t.the-answer@hotmail.co.jp
url = https://github.com/biopackathon/python-packaging-exercise
keywords = keyword1, keyword2
license_file = LICENSE
classifiers =
    License :: OSI Approved :: MIT License
    Natural Language :: English
    Operating System :: OS Independent
    Programming Language :: Python :: 3
    Topic :: Scientific/Engineering :: Bio-Informatics

[options]
packages = mypackageabc
python_requires = >=3.12
install_requires = numpy

[options.packages.find]
packages = mypackageabc
```

以前はこのようなメタデータは`setup.py`内部に直接書いていたみたいですが、こちらの方が見やすく、管理しやすいかと思います。

# 3. テスト

`tests`ディレクトリを切り、その中に`test_my_array.py`と`test_my_func.py`を以下のように作成しました。

```py
# test_my_array.py
import numpy as np
from mypackageabc.my_module import my_array, my_func

def test_my_array_type():
    assert type(my_array) == np.ndarray

def test_my_array_value():
    for element in my_array:
        assert isinstance(element, str)
```

```py
# test_my_func.py
import numpy as np
from mypackageabc.my_module import my_array, my_func

def test_my_func_type():
    assert callable(my_func)

def test_my_func_value():
    values = my_func(my_array)
    for element in values:
        assert type(element) == np.int64
```

また`pytest`にディレクトリを認識してもらうために、空の`__init__.py`も`tests`内に設置しておきました。

なお、`pytest`は以下のように実行します。

上記のように`test_`から始まる関数がテストの実行対象となります。

```shell
python -m pytest -v
(packaging) koki@tsuyusaacstudio setuptools % python -m pytest -v
# ==================================== test session starts ====================================
# platform darwin -- Python 3.12.1, pytest-8.0.0, pluggy-1.4.0 -- /Users/koki/mambaforge/envs/packaging/bin/python
# cachedir: .pytest_cache
# rootdir: /Users/koki/Desktop/elwood/Dev/python-packaging-exercise/setuptools
# collected 4 items

# tests/test_my_array.py::test_my_array_type PASSED                                     [ 25%]
# tests/test_my_array.py::test_my_array_value PASSED                                    [ 50%]
# tests/test_my_func.py::test_my_func_type PASSED                                       [ 75%]
# tests/test_my_func.py::test_my_func_value PASSED                                      [100%]

# ===================================== 4 passed in 0.43s =====================================
```

これにより、全てのテストが正常に実行されたことがわかります。
`pytest-cov`を使うと、さらにカバレッジ（実装したコードの何%がテストされたか）を見積もることができます。

以下のように、`--cov`の後に自分のパッケージ名を指定するだけです。

```shell
python -m pytest -v --cov=mypackageabc
# ==================================== test session starts ====================================
# platform darwin -- Python 3.10.9, pytest-7.4.4, pluggy-1.3.0 -- /Users/koki/mambaforge/bin/python
# cachedir: .pytest_cache
# rootdir: /Users/koki/Desktop/elwood/Dev/python-packaging-exercise/setuptools_twine
# plugins: cov-4.1.0, anyio-4.2.0
# collected 4 items

# tests/test_my_array.py::test_my_array_type PASSED                                     [ 25%]
# tests/test_my_array.py::test_my_array_value PASSED                                    [ 50%]
# tests/test_my_func.py::test_my_func_type PASSED                                       [ 75%]
# tests/test_my_func.py::test_my_func_value PASSED                                      [100%]

# ---------- coverage: platform darwin, python 3.10.9-final-0 ----------
# Name                        Stmts   Miss  Cover
# -----------------------------------------------
# mypackageabc/__init__.py        1      0   100%
# mypackageabc/my_module.py       5      0   100%
# -----------------------------------------------
# TOTAL                           6      0   100%
```

# 4. インストール

以下のようにして、Pythonに自作のパッケージをインストールします。

```shell
pip install -e .
```

## 補足: Editable Install
上記の`-e`の部分は、editable installというもので、通常であればインストールされたPythonパッケージは、`site-packages`というディレクトリ（例: `conda`環境であれば`/Users/koki/mambaforge/envs/packaging/lib/python3.12/site-packages`みたいなパス）に配置されますが、このオプションをつけることにより、優先的に現在開発中のパッケージの方がインストールされます。

一度editableモードでインストールされたパッケージは、再度インストールコマンドを叩かなくても、Pythonを再起動するだけで、変更したソースコードを直ちにPythonインタプリタ上で実行することができるようになるため、パッケージ開発時に推奨されます。

editable installは、`python setup.py develop`（さらに旧式のコマンド）や、`poetry install`など、他のパッケージ開発フローでも実装されています。

`pip list`を実行すると、以下のように自分のパッケージだけ、現在の作業ディレクトリが参照されていることがわかります。

```shell
pip list
# ...（省略）...
msgpack            1.0.7
mypackageabc       0.99.0     /Users/koki/Desktop/elwood/Dev/python-packaging-exercise/setuptools_twine
mypy-extensions    1.0.0
# ...（省略）...
```

# 5. ビルド

PyPI向けに公開できる配布物として体裁を整えるために、以下のようなコードを実行します。

## 5.1 ソースコードを生成する場合

ソースコードをZIPファイルにする場合、以下のように実行します。

```shell
python setup.py sdist
```

## 5.2 Wheelファイルを生成する場合

オフラインでも直ちにPythonにインストールできる標準フォーマットWheelの形式でパッケージを出力する場合、以下のように実行します。

```shell
python setup.py bdist_wheel
```

なお、これら2つのコードは、以下のコードで一度に行えます。

```shell
python -m build
```

これにより、以下のようなファイルが生成されます。

```shell
ls dist
# mypackageabc-0.99.0-py3-none-any.whl	mypackageabc-0.99.0.tar.gz
```

[Python Packaging User Guide](https://packaging.python.org/ja/latest/discussions/setup-py-deprecated/)としては、こちらの書き方を推奨するとのことです。

# 6. 配布

`twine`コマンドを使って、作成したパッケージをTestPyPI(練習用レポジトリ)
やPyPI(練習用レポジトリ)に公開します。

事前にアカウント登録をして、APIトークンを取得後、以下のようにして、作成したパッケージをTestPyPIのサーバーに転送します。
（既に存在する名前のパッケージは登録できないので、事前に確認しておきましょう）

```
twine upload --repository-url https://test.pypi.org/legacy/ dist/* -u "__token__" -p "＜APIトークン＞"
```

これにより、

https://test.pypi.org/project/mypackageabc/

のようなWebサイトが作成され、

```shell
pip install -i https://test.pypi.org/simple/ mypackageabc
```

で、作成したパッケージが、誰でも使えるようになりました。

本番では、`twine upload`の`--repository-url https://test.pypi.org/legacy/`の部分を省略することで、PyPIの方にパッケージが登録されるようになります。

# 7. CI

最後に、GitHub Actionsを使って、CI（継続的インテグレーション）を実施します。

ここでは、上記の`pytest`による単体テストや`flake8`によるコードチェックの自動実行を行う`python-package.yml`（*）というワークフローを一部改変して利用しました。

* [Actions/Choose a workflow](https://github.com/biopackathon/python-packaging-exercise/actions/new)のページで推薦されたもの

それ以外にも、(Test)PyPIへのリリースの自動化を行う`python-publish.yml`や、Release PleaseでGitHubのリリースノートを自動更新するのも良いでしょう（cf. [GitHub Releaseの解説 @ Bio”Pack”athon2023#01](https://togotv.dbcls.jp/en/20230116.html)）