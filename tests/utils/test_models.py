import unittest
from src.utils.constants import ID, PATTERN, MESSAGE, SEVERITY, INFO, REGEX, ADDITIONAL_PROPERTIES
from src.utils.models import InlineRule


class TestInlineRule(unittest.TestCase):
    def test_from_dict_successful_minimal(self):
        rule_data = {
            ID: "no-print",
            PATTERN: "print(",
            MESSAGE: "Avoid print statements"
        }
        rule = InlineRule.from_dict(rule_data)

        self.assertEqual(rule.id, "no-print")
        self.assertEqual(rule.pattern, "print(")
        self.assertEqual(rule.message, "Avoid print statements")
        self.assertEqual(rule.severity, INFO)
        self.assertFalse(rule.regex)
        self.assertEqual(rule.additional_properties, {})

    def test_from_dict_successful_full(self):
        rule_data = {
            ID: "todo-comment",
            PATTERN: "# TODO",
            MESSAGE: "Remove TODO before merge",
            SEVERITY: "warning",
            REGEX: True,
            ADDITIONAL_PROPERTIES: {"context": "comment"}
        }
        rule = InlineRule.from_dict(rule_data)

        self.assertEqual(rule.id, "todo-comment")
        self.assertEqual(rule.pattern, "# TODO")
        self.assertEqual(rule.message, "Remove TODO before merge")
        self.assertEqual(rule.severity, "warning")
        self.assertTrue(rule.regex)
        self.assertEqual(rule.additional_properties, {"context": "comment"})

    def test_missing_required_fields(self):
        with self.assertRaises(ValueError) as ctx:
            InlineRule.from_dict({PATTERN: "x", MESSAGE: "msg"})
        self.assertIn(ID, str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            InlineRule.from_dict({ID: "rule", MESSAGE: "msg"})
        self.assertIn(PATTERN, str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            InlineRule.from_dict({ID: "rule", PATTERN: "x"})
        self.assertIn(MESSAGE, str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
