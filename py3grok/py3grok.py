import os
from copy import copy
from typing import Any, Dict, List, Optional
import pkg_resources
import regex

DEFAULT_PATTERNS_DIR = [pkg_resources.resource_filename(__name__, "patterns")]


class GrokPattern:
    def __init__(self, pattern_name: str, regex_str: str) -> None:
        self.pattern_name: str = pattern_name
        self.regex_str: str = regex_str

    def __str__(self) -> str:
        return f"GrokPattern ({self.pattern_name}, {self.regex_str})"

    def __repr__(self) -> str:
        return self.pattern_name

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, GrokPattern):
            return False
        return (self.pattern_name, self.regex_str) == (__o.pattern_name, __o.regex_str)

    def __hash__(self) -> int:
        return hash((self.pattern_name, self.regex_str))


class Grok:
    def __init__(self, pattern: str, available_patterns: dict = None, **kwargs) -> None:
        self.available_patterns: dict = available_patterns if available_patterns else {}
        self.compiled_pattern: Optional[regex.Pattern] = None
        self._pattern: str = ""
        self._type_mapper: dict = {}
        self._extra_args = kwargs
        # Set and compile given pattern.
        self.pattern = pattern

    def __str__(self) -> str:
        return f"Grok ({self.pattern})"

    def __repr__(self) -> str:
        return self.pattern

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Grok):
            return False
        return (self.pattern, frozenset(self.available_patterns.items())) == (
            __o.pattern,
            frozenset(__o.available_patterns.items()),
        )

    def __hash__(self) -> int:
        return hash(frozenset(self.available_patterns.items()))

    @property
    def pattern(self) -> str:
        """Returns the current pattern used in this instance of ``Grok``."""
        return self._pattern

    @pattern.setter
    def pattern(self, pattern) -> None:
        self._pattern = pattern
        self._compile_pattern()

    def set_pattern(self, pattern) -> None:
        """
        Convienence function that changes the pattern. This is equivalent to
        calling ``grok.pattern = pattern``.
        """
        self.pattern = pattern

    def _compile_pattern(self) -> None:
        """
        Private function that compiles specified pattern into a ``Regex.Pattern``
        which is accessible by ``self.compiled_pattern`` after executing this function.
        """
        self._type_mapper = {}
        pattern = copy(self.pattern)

        while True:
            matches = regex.findall(r"%{(\w+):(\w+):(\w+)}", pattern)
            for match in matches:
                self._type_mapper[match[1]] = match[2]

            # Replace %{pattern_name:custom_name} (or %{pattern_name:custom_name:type}
            # with regex pattern and group name.
            pattern = regex.sub(
                r"%{(\w+):(\w+)(?::\w+)?}",
                lambda m: f"(?P<{m.group(2)}>{self.available_patterns[m.group(1)].regex_str})",
                pattern,
            )
            # Replace %{pattern_name} with regex pattern.
            pattern = regex.sub(
                r"%{(\w+)}",
                lambda m: f"({self.available_patterns[m.group(1)].regex_str})",
                pattern,
            )
            if regex.search(r"%{\w+(:\w+)?}", pattern) is None:
                break

        self.compiled_pattern = regex.compile(pattern, **self._extra_args)

    def match(self, text: str, full_match: bool = True) -> Optional[Dict[str, Any]]:
        """
        If text is matched with pattern, return variable names specified
        (%{pattern:variable name}) in pattern and their corresponding values.
        If not matched, return None.
        """
        if not self.compiled_pattern:
            return None

        match_object: Optional[regex.Match] = None
        if full_match:
            match_object = self.compiled_pattern.fullmatch(text)
        else:
            match_object = self.compiled_pattern.search(text)

        if match_object is None:
            return None
        matches = match_object.groupdict()

        for key, match in matches.items():
            try:
                if self._type_mapper[key] == "int":
                    matches[key] = int(match)
                if self._type_mapper[key] == "float":
                    matches[key] = float(match)
            except (TypeError, KeyError) as _:
                pass

        return matches


class GrokEnvironment:
    def __init__(self, custom_dirs: List[str] = None):
        """
        The ``GrokEnvironment`` is a factory class that loads grok pattern files
        and creates new instances of ``Grok`` for pattern matching. You will only
        need to have **one** instance of this class and use the method,
        ``GrokEnvironment.create()`` to create ``Grok`` instances.

        Custom directories can be used if you want to load your own grok
        pattern files.
        """
        self.custom_dirs = None
        self.available_patterns = {}

        if custom_dirs:
            DEFAULT_PATTERNS_DIR.extend(custom_dirs)

        for directory in DEFAULT_PATTERNS_DIR:
            for f in os.listdir(directory):
                patterns = self.load_patterns_from_file(os.path.join(directory, f))
                self.available_patterns.update(patterns)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, GrokEnvironment):
            return False
        return (frozenset(__o.available_patterns.items())) == (
            frozenset(self.available_patterns.items()),
        )

    def __hash__(self) -> int:
        return hash(frozenset(self.available_patterns.items()))

    def create(self, pattern: str, **kwargs) -> Grok:
        """
        Create a new instance of ``Grok`` for pattern matching. You can also pass
        ``flags=re.IGNORECASE`` or other flags for regex configuration if needed.
        """
        return Grok(pattern, available_patterns=self.available_patterns, **kwargs)

    @staticmethod
    def load_patterns_from_file(file: str) -> dict:
        """
        Load patterns from a given file. Instiates each line as an individual
        ``GrokPattern`` object that can be accessed from ``self.available_patterns``.
        """
        patterns = {}

        with open(file, "r", encoding="utf-8") as f:
            lines = filter(lambda l: (l.strip() != "" and l[0] != "#"), f.readlines())
            for l in lines:
                sep = l.find(" ")
                name = l[:sep]
                patterns[name] = GrokPattern(name, l[sep:].strip())

        return patterns
