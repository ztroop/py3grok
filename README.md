[![Build Status](https://github.com/ztroop/py3grok/actions/workflows/build.yml/badge.svg)](https://github.com/ztroop/py3grok/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/ztroop/py3grok/branch/master/graph/badge.svg?token=9IMVSWC2GH)](https://codecov.io/gh/ztroop/py3grok)

# py3grok

A Python library to parse strings and extract information from structured or unstructured data. This library is based on [pygrok](https://github.com/garyelephant/pygrok).

## Why?

* Parsing and matching patterns from a string.
* Relieving from complex regular expressions.
* Extracting information from structured/unstructured data.

## Installation

```sh
pip install py3grok
```

## Getting Started

```python
from py3grok import Grok

grok = Grok()
text = 'gary is male, 25 years old and weighs 68.5 kilograms'
grok.set_pattern('%{WORD:name} is %{WORD:gender}, %{NUMBER:age} years old and weighs %{NUMBER:weight} kilograms')
print(grok.match(text))

# {'gender': 'male', 'age': '25', 'name': 'gary', 'weight': '68.5'}
```

Numbers can be converted from string to `int` or `float` if you use `%{pattern:name:type}` syntax, such as `%{NUMBER:age:int}`

```python
from py3grok import Grok

grok = Grok()
text = 'gary is male, 25 years old and weighs 68.5 kilograms'
grok.set_pattern('%{WORD:name} is %{WORD:gender}, %{NUMBER:age:int} years old and weighs %{NUMBER:weight:float} kilograms')
print(grok.match(text))

# {'gender': 'male', 'age': 25, 'name': 'gary', 'weight': 68.5}
```

Now `age` is of type `int` and `weight` is of type `float`.

See all available patterns [here](./py3grok/patterns)!

## Additional Notes

The python `re` module does not support regular expression syntax atomic grouping `(?>)`, so pygrok requires [regex](https://pypi.python.org/pypi/regex) to be installed.

Grok is a simple software that allows you to easily parse strings, logs and other files. With grok, you can turn unstructured log and event data into structured data.

I recommend you to have a look at [logstash filter grok](https://www.elastic.co/guide/en/logstash/current/plugins-filters-grok.html), it explains how Grok works.

Pattern files come from [logstash filter grok's pattern files](https://github.com/logstash-plugins/logstash-patterns-core/tree/master/patterns)
