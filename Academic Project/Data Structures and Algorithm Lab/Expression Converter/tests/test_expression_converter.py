import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.stack import Stack
from src.converter import ExpressionConverter
from src.evaluator import ExpressionEvaluator


class TestStack(unittest.TestCase):
    def test_stack_push_pop_peek(self):
        s = Stack()
        self.assertTrue(s.is_empty())
        s.push(10)
        s.push(20)
        self.assertEqual(s.size(), 2)
        self.assertEqual(s.peek(), 20)
        self.assertEqual(s.pop(), 20)
        self.assertEqual(s.pop(), 10)
        self.assertTrue(s.is_empty())


class TestExpressionConverter(unittest.TestCase):
    def test_infix_to_postfix_basic(self):
        self.assertEqual(ExpressionConverter.infix_to_postfix("A + B * C"), "A B C * +")
        self.assertEqual(ExpressionConverter.infix_to_postfix("(A + B) * C"), "A B + C *")

    def test_infix_to_prefix_basic(self):
        self.assertEqual(ExpressionConverter.infix_to_prefix("A + B * C"), "+ A * B C")
        self.assertEqual(ExpressionConverter.infix_to_prefix("(A + B) * C"), "* + A B C")

    def test_postfix_to_infix(self):
        self.assertEqual(ExpressionConverter.postfix_to_infix("A B + C *"), "((A + B) * C)")

    def test_mismatched_parentheses(self):
        with self.assertRaises(ValueError):
            ExpressionConverter.infix_to_postfix("(A + B * C")


class TestExpressionEvaluator(unittest.TestCase):
    def test_evaluate_postfix_numeric(self):
        # 3 5 2 * + => 3 + (5 * 2) = 13
        self.assertEqual(ExpressionEvaluator.evaluate_postfix("3 5 2 * +"), 13)

    def test_evaluate_infix_complex(self):
        # (10 + 20) / (3 * 2) + 2 ^ 3 => 30 / 6 + 8 = 5 + 8 = 13
        self.assertEqual(ExpressionEvaluator.evaluate_infix("(10 + 20) / (3 * 2) + 2 ^ 3"), 13)

    def test_zero_division(self):
        with self.assertRaises(ZeroDivisionError):
            ExpressionEvaluator.evaluate_infix("10 / 0")


if __name__ == "__main__":
    unittest.main()
