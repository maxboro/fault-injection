import unittest
from unittest.mock import patch

from src.fault_injection import raise_, raise_random


class TestRaiseDecorator(unittest.TestCase):
    def test_raise_always_raises_runtime_error_when_enabled(self):
        @raise_()
        def add(a, b):
            return a + b

        with self.assertRaisesRegex(RuntimeError, "raise_ exception is raised"):
            add(1, 2)

    def test_raise_disable_calls_wrapped_function(self):
        @raise_(disable=True)
        def add(a, b):
            return a + b

        self.assertEqual(add(2, 3), 5)

    def test_raise_preserves_metadata_with_wraps(self):
        @raise_(disable=True)
        def add(a, b):
            return a + b

        self.assertEqual(add.__name__, "add")


class TestRaiseRandomDecorator(unittest.TestCase):
    def test_raise_random_rejects_invalid_probability(self):
        with self.assertRaisesRegex(ValueError, "prob_of_raise should be 0-1"):
            raise_random(-0.01)

        with self.assertRaisesRegex(ValueError, "prob_of_raise should be 0-1"):
            raise_random(1.01)

    def test_raise_random_raises_when_random_value_is_below_threshold(self):
        with patch("src.fault_injection.raise_exception.random.random", return_value=0.19):
            @raise_random(prob_of_raise=0.2)
            def add(a, b):
                return a + b

            with self.assertRaisesRegex(RuntimeError, "random_raise exception is raised"):
                add(1, 2)

    def test_raise_random_calls_wrapped_function_when_random_value_is_above_threshold(self):
        with patch("src.fault_injection.raise_exception.random.random", return_value=0.9):
            @raise_random(prob_of_raise=0.2)
            def add(a, b):
                return a + b

            self.assertEqual(add(3, 4), 7)

    def test_raise_random_disable_skips_random_and_raising(self):
        with patch(
            "src.fault_injection.raise_exception.random.random",
            side_effect=AssertionError("random.random should not be called when disabled"),
        ):
            @raise_random(prob_of_raise=1.0, disable=True)
            def add(a, b):
                return a + b

            self.assertEqual(add(10, 5), 15)


if __name__ == "__main__":
    unittest.main()
