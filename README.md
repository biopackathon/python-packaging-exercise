# python-packaging-exercise
Pythonパッケージ開発の練習

## init/
- Python言語においてパッケージ = ディレクトリ、モジュール = ファイルであることを実感する
- `__init__.py`, `__all__`, サブパッケージを習得する

Pythonパッケージは、ビルドの仕方に関して以下の3つに大別されるため、各々のやり方を試す

## 1. setuptools/
- `setuptools.setup`を中心としたやり方
- 関連ファイル

## 2. build/
- `python -m build`を中心としたやり方

## 3. poetry/
- `poetry`コマンドでパッケージングを一元管理するやり方
