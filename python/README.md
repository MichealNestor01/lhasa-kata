# Python Quick-Start

Make sure you install the following dependencies into your Python environment:

```
pip install setuptools
pip install xmltodict
pip install beautifulsoup4
```

The example code uses xmltodict, but you might find Beautiful Soup easier to use, depending on how you write your code. If you decide to use only one, then remember to remove the other from `setup.py`.

# run code:

open `python` directory.

Setup:

```
$ python -m venv .env
$ source .env/bin/activate
$ pip install .
```

Running tests: `$ python -m unittest tests.kata_test`

Running code: `$ python src/lhasakata/kata.py`
