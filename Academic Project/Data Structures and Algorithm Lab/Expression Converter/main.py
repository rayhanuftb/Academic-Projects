#!/usr/bin/env python3
"""
CLI Tool for Expression Converter and Evaluator.
Course: Data Structures and Algorithm Lab (ICT 4156)
"""

import sys
import argparse
from src.converter import ExpressionConverter
from src.evaluator import ExpressionEvaluator


def main():
    parser = argparse.ArgumentParser(description="Expression Converter and Arithmetic Evaluator")
    parser.add_argument("--infix", type=str, default=None, help="Infix expression to convert and evaluate (e.g. '3 + 5 * (2 ^ 3)')")
    parser.add_argument("--postfix", type=str, default=None, help="Postfix expression to evaluate (e.g. '3 5 2 3 ^ * +')")

    args = parser.parse_args()

    print("\n==========================================================")
    print("  Expression Converter & Evaluator - Data Structures Lab  ")
    print("==========================================================")

    sample_expr = args.infix if args.infix else "((A + B) * C) - (D / E ^ F)"
    
    if args.postfix:
        print(f"\n[+] Input Postfix Expression : {args.postfix}")
        try:
            val = ExpressionEvaluator.evaluate_postfix(args.postfix)
            print(f"  * Evaluated Numerical Value: {val}")
            infix_repr = ExpressionConverter.postfix_to_infix(args.postfix)
            print(f"  * Reconstructed Infix Form : {infix_repr}")
        except Exception as e:
            print(f"[-] Evaluation Error: {e}", file=sys.stderr)
    else:
        print(f"\n[+] Input Infix Expression   : {sample_expr}")
        try:
            postfix = ExpressionConverter.infix_to_postfix(sample_expr)
            prefix = ExpressionConverter.infix_to_prefix(sample_expr)
            print(f"  * Postfix (RPN) Notation   : {postfix}")
            print(f"  * Prefix (Polish) Notation : {prefix}")

            # If expression has numeric terms, evaluate
            if any(char.isdigit() for char in sample_expr):
                result = ExpressionEvaluator.evaluate_infix(sample_expr)
                print(f"  * Evaluated Numerical Value: {result}")
        except Exception as e:
            print(f"[-] Conversion Error: {e}", file=sys.stderr)

    print("\n[✓] Expression operation completed successfully.\n")


if __name__ == "__main__":
    main()
