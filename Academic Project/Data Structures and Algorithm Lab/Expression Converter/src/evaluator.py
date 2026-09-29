from .stack import Stack
from .converter import ExpressionConverter


class ExpressionEvaluator:
    """Evaluates arithmetic expressions with full operator support and zero-division protection."""

    @staticmethod
    def evaluate_postfix(postfix_expr: str) -> float:
        """
        Evaluates a space-separated postfix expression.
        Time Complexity: O(N) | Space Complexity: O(N)
        """
        tokens = postfix_expr.strip().split()
        if not tokens:
            raise ValueError("Empty expression.")
        stack = Stack()

        for token in tokens:
            if token in {'+', '-', '*', '/', '^'}:
                if stack.size() < 2:
                    raise ValueError(f"Insufficient operands for operator '{token}'")
                b = stack.pop()
                a = stack.pop()

                if token == '+':
                    stack.push(a + b)
                elif token == '-':
                    stack.push(a - b)
                elif token == '*':
                    stack.push(a * b)
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero encountered in expression.")
                    stack.push(a / b)
                elif token == '^':
                    stack.push(a ** b)
            else:
                try:
                    stack.push(float(token))
                except ValueError:
                    raise ValueError(f"Cannot evaluate non-numeric variable '{token}' numerically.")

        if stack.size() != 1:
            raise ValueError("Malformed expression.")
        res = stack.pop()
        return int(res) if res.is_integer() else round(res, 4)

    @staticmethod
    def evaluate_infix(infix_expr: str) -> float:
        """Converts Infix to Postfix and evaluates the result."""
        postfix = ExpressionConverter.infix_to_postfix(infix_expr)
        return ExpressionEvaluator.evaluate_postfix(postfix)
