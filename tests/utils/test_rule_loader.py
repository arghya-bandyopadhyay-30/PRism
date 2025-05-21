import unittest
import tempfile
import yaml
import os

from src.utils.models import InlineRule
from src.utils.constants import ID, PATTERN, MESSAGE, SEVERITY, REGEX
from src.utils.rule_loader import load_inline_rules


class TestRuleLoader(unittest.TestCase):

    def setUp(self):
        self.sample_rules = {
            "inline_rules": [
                {
                    ID: "no-print",
                    PATTERN: "print(",
                    MESSAGE: "Avoid using print statements",
                    SEVERITY: "warning"
                },
                {
                    ID: "todo-comment",
                    PATTERN: "# TODO",
                    MESSAGE: "Resolve TODO before merge",
                    REGEX: True
                }
            ]
        }

        self.temp_file = tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".yaml")
        yaml.dump(self.sample_rules, self.temp_file)
        self.temp_file.close()

    def tearDown(self):
        os.unlink(self.temp_file.name)

    def test_load_inline_rules_successfully(self):
        rules = load_inline_rules(self.temp_file.name)
        self.assertIsInstance(rules, list)
        self.assertEqual(len(rules), 2)

        first_rule = rules[0]
        self.assertIsInstance(first_rule, InlineRule)
        self.assertEqual(first_rule.id, "no-print")
        self.assertEqual(first_rule.pattern, "print(")
        self.assertEqual(first_rule.message, "Avoid using print statements")
        self.assertEqual(first_rule.severity, "warning")
        self.assertFalse(first_rule.regex)

        second_rule = rules[1]
        self.assertTrue(second_rule.regex)
        self.assertEqual(second_rule.id, "todo-comment")

    def test_load_inline_rules_missing_key(self):
        with open(self.temp_file.name, "w") as f:
            yaml.dump({"not_rules": []}, f)

        rules = load_inline_rules(self.temp_file.name)
        self.assertEqual(rules, [])


if __name__ == "__main__":
    unittest.main()
