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

When using this library, you will want to first create an instance of `GrokEnvironment`.
That will load the default and custom grok pattern files. Whenever you want to create a new
pattern, you can run `GrokEnvironment.create(pattern)` which returns an instance of `Grok`,
where you can simply run `Grok.match(text)`.

For flexibility, you can also modify a `Grok` instance's `pattern` property as well if needed.

### Code Example

```python
from py3grok import GrokEnvironment

grok_env = GrokEnvironment()
pattern = '%{WORD:name} is %{WORD:gender}, %{NUMBER:age} years old and weighs %{NUMBER:weight} kilograms.'

# Regex flags can be used, like: grok_env.create(pattern, flags=re.IGNORECASE)
grok = grok_env.create(pattern)

text = 'Gary is male, 25 years old and weighs 68.5 kilograms.'
print(grok.match(text))

# {'gender': 'male', 'age': '25', 'name': 'Gary', 'weight': '68.5'}
```

Numbers can be converted from string to `int` or `float` if you use `%{pattern:name:type}` syntax, such as `%{NUMBER:age:int}`

See all available patterns [here](./py3grok/patterns)!

## Additional Notes

The python `re` module does not support regular expression syntax atomic grouping `(?>)`, so pygrok requires [regex](https://pypi.python.org/pypi/regex) to be installed.

Grok is a simple software that allows you to easily parse strings, logs and other files. With grok, you can turn unstructured log and event data into structured data.

I recommend you to have a look at [logstash filter grok](https://www.elastic.co/guide/en/logstash/current/plugins-filters-grok.html), it explains how Grok works.

Pattern files come from [logstash filter grok's pattern files](https://github.com/logstash-plugins/logstash-patterns-core/tree/master/patterns).