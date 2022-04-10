from unittest import TestCase
from py3grok import Grok
from py3grok.py3grok import GrokPattern


class TestGrok(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_grok(self):
        grok = Grok()

        text = "gary is male, 25 years old and weighs 68.5 kilograms"
        pattern = "%{WORD:name} is %{WORD:gender}, %{NUMBER:age:int} years old and weighs %{NUMBER:weight:float} kilograms"

        grok.pattern = pattern
        result = grok.match(text)
        expected_result = {"name": "gary", "gender": "male", "age": 25, "weight": 68.5}

        self.assertEqual(result, expected_result)

        grok.set_pattern(
            "%{WORD:name} is %{WORD:gender} and %{NUMBER:age:int} years old"
        )
        result = grok.match("allie is female and 32 years old")
        expected_result = {"age": 32, "gender": "female", "name": "allie"}

        self.assertEqual(result, expected_result)

    def test_grok_available_patterns(self):
        grok = Grok()

        self.assertEqual(len(grok.available_patterns), 361)

    def test_grok__eq__comparison(self):
        grok1 = Grok()
        grok2 = Grok()
        grokpattern1 = GrokPattern("test_name", "regex")
        grokpattern2 = GrokPattern("test_name", "regex")
        grokpattern3 = GrokPattern("other_name", "diff")

        self.assertEqual(grok1, grok2)
        self.assertNotEqual(grok1, grokpattern1)

        grok1.set_pattern("%{WORD:name}")
        self.assertNotEqual(grok1, grok2)

        self.assertEqual(grokpattern1, grokpattern2)
        self.assertNotEqual(grokpattern1, grokpattern3)
        self.assertNotEqual(grokpattern1, grok1)
