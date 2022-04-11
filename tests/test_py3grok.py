from unittest import TestCase
from py3grok import Grok, GrokEnvironment, GrokPattern
from re import IGNORECASE


class TestGrok(TestCase):
    def setUp(self) -> None:
        self.grok_env = GrokEnvironment()

    def test_grok(self):
        text = "gary is male, 25 years old."
        pattern = "%{WORD:name} is %{WORD:gender}, %{NUMBER:age:int} years old."
        grok = self.grok_env.create(pattern)
        result = grok.match(text)
        expected_result = {"age": 25, "gender": "male", "name": "gary"}

        self.assertEqual(result, expected_result)
        self.assertEqual(len(grok.available_patterns), 361)

    def test_grok_modify_pattern(self):
        text = "gary is male, 25 years old."
        pattern = "%{WORD:name} is %{WORD:gender}, %{NUMBER:age:int} years old."
        grok = self.grok_env.create(pattern)
        grok.set_pattern("something else")

        self.assertEqual(grok.pattern, "something else")

    def test_grok_ignore_case(self):
        text = "gary is male, 25 years old."
        pattern = "%{WORD:name} IS %{WORD:gender}, %{NUMBER:age:int} YEARS OLD."
        grok = self.grok_env.create(pattern, flags=IGNORECASE)
        result = grok.match(text)
        expected_result = {"age": 25, "gender": "male", "name": "gary"}

        self.assertEqual(result, expected_result)

    def test_magic_methods(self):
        grok1 = Grok("test pattern")
        grok2 = Grok("test pattern")
        grok3 = Grok("another pattern")

        grokpattern1 = GrokPattern("TEST", "regex")
        grokpattern2 = GrokPattern("TEST", "regex")
        grokpattern3 = GrokPattern("OTHER", "diff")

        grok_set = {grok1, grok2, grok3}
        grok_pattern_set = {grokpattern1, grokpattern2, grokpattern3}

        self.assertEqual(grok1, grok2)
        self.assertNotEqual(grok1, grok3)

        self.assertEqual(grokpattern1, grokpattern2)
        self.assertNotEqual(grokpattern1, grokpattern3)
        self.assertNotEqual(grokpattern1, grok1)

        self.assertIsInstance(grok_set, set)
        self.assertIsInstance(grok_pattern_set, set)

        self.assertEqual(str(grok1), "Grok (test pattern)")
        self.assertEqual(repr(grok1), "test pattern")

        self.assertEqual(str(grokpattern1), "GrokPattern (TEST, regex)")
        self.assertEqual(repr(grokpattern1), "TEST")
