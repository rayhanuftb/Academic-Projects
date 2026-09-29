import re
from typing import List
from .stack import Stack

PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
RIGHT_ASSOCIATIVE = {'^'}


class ExpressionConverter:
    """Implements conversion between Infix, Postfix (RPN), and Prefix (Polish) notations."""

    @staticmethod
    def tokenize(expression: str) -> List[str]:
        """Splits an expression string into operators, parentheses, and multi-digit operands."""
        if not expression or not expression.strip():
            return []
        pattern = r'\d+\.?\d*|[a-zA-Z]+|[\+\-\*\/\^\(\)]'
        tokens = re.findall(pattern, expression.strip())
        return tokens

    @staticmethod
    def infix_to_postfix(expression: str) -> str:
        """
        Converts an Infix expression to Postfix notation using Dijkstra's Shunting-Yard algorithm.
        Time Complexity: O(N) | Space Complexity: O(N)
        """
        tokens = ExpressionConverter.tokenize(expression)
        if not tokens:
            raise ValueError("Expression is empty.")

        output: List[str] = []
        stack = Stack()

        for token in tokens:
            if token.isalnum() or token.replace('.', '', 1).isdigit():
                output.append(token)
            elif token == '(':
                stack.push(token)
            elif token == ')':
                while not stack.is_empty() and stack.peek() != '(':
                    output.append(stack.pop())
                if stack.is_empty() or stack.peek() != '(':
                    raise ValueError("Mismatched parentheses in expression.")
                stack.pop()  # Pop '('
            elif token in PRECEDENCE:
                while not stack.is_empty() and stack.peek() in PRECEDENCE:
                    top_op = stack.peek()
                    if (token not in RIGHT_ASSOCIATIVE and PRECEDENCE[top_op] >= PRECEDENCE[token]) or \
                       (token in RIGHT_ASSOCIATIVE and PRECEDENCE[top_op] > PRECEDENCE[token]):
                        output.append(stack.pop())
                    else:
                        break
                stack.push(token)
            else:
                raise ValueError(f"Invalid character/token: {token}")

        while not stack.is_empty():
            top = stack.pop()
            if top == '(':
                raise ValueError("Mismatched parentheses in expression.")
            output.append(top)

        return " ".join(output)

    @staticmethod
    def infix_to_prefix(expression: str) -> str:
        """
        Converts Infix to Prefix by reversing tokens, swapping brackets, running Shunting-Yard, and reversing output.
        Time Complexity: O(N) | Space Complexity: O(N)
        """
        tokens = ExpressionConverter.tokenize(expression)
        if not tokens:
            raise ValueError("Expression is empty.")

        # Reverse tokens and swap '(' with ')'
        reversed_tokens = []
        for t in reversed(tokens):
            if t == '(':
                reversed_tokens.append(')')
            elif t == ')':
                reversed_tokens.append('(')
            else:
                reversed_tokens.append(t)

        reversed_infix = " ".join(reversed_tokens)
        postfix_rev = ExpressionConverter.infix_to_postfix(reversed_infix)
        prefix_tokens = postfix_rev.split()[::-1]
        return " ".join(prefix_tokens)

    @staticmethod
    def postfix_to_infix(expression: str) -> str:
        """Converts Postfix notation to parenthesized Infix."""
        tokens = expression.strip().split()
        if not tokens:
            raise ValueError("Expression is empty.")
        stack = Stack()

        for token in tokens:
            if token in PRECEDENCE:
                if stack.size() < 2:
                    raise ValueError(f"Insufficient operands for operator '{token}'")
                op2 = stack.pop()
                op1 = stack.pop()
                stack.push(f"({op1} {token} {op2})")
            else:
                stack.push(token)

        if stack.size() != 1:
            raise ValueError("Malformed postfix expression.")
        return stack.pop()
