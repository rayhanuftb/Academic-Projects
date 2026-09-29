"""Tests for SafeRx AI validation module."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import pytest
from saferx.validation import InputValidator


class TestInputValidator:
    def test_valid_medication_name(self):
        valid, msg = InputValidator.validate_medication_name("aspirin")
        assert valid is True

    def test_empty_medication_name(self):
        valid, msg = InputValidator.validate_medication_name("")
        assert valid is False
        assert "empty" in msg.lower()

    def test_short_medication_name(self):
        valid, msg = InputValidator.validate_medication_name("a")
        assert valid is False

    def test_valid_age(self):
        valid, msg = InputValidator.validate_age(25)
        assert valid is True

    def test_invalid_age_negative(self):
        valid, msg = InputValidator.validate_age(-5)
        assert valid is False

    def test_invalid_age_too_high(self):
        valid, msg = InputValidator.validate_age(200)
        assert valid is False

    def test_valid_weight(self):
        valid, msg = InputValidator.validate_weight(70.5)
        assert valid is True

    def test_invalid_weight_zero(self):
        valid, msg = InputValidator.validate_weight(0)
        assert valid is False

    def test_valid_medication_list(self):
        valid, msg = InputValidator.validate_medication_list(["aspirin", "metformin"])
        assert valid is True

    def test_empty_medication_list(self):
        valid, msg = InputValidator.validate_medication_list([])
        assert valid is False

    def test_sanitize_input(self):
        result = InputValidator.sanitize_input("<script>alert('xss')</script>")
        assert "<" not in result
        assert ">" not in result

    def test_sanitize_empty(self):
        result = InputValidator.sanitize_input("")
        assert result == ""
