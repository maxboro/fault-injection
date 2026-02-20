import unittest
from unittest.mock import patch

from fault_injection import (
    raise_,
    raise_inline,
    raise_random,
    raise_random_inline,
    raise_at_nth_call,
    raise_at_nth_call_inline
)


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

    def test_raise_uses_custom_message(self):
        @raise_(msg="custom raise message")
        def add(a, b):
            return a + b

        with self.assertRaisesRegex(RuntimeError, "custom raise message"):
            add(1, 2)


class TestRaiseInline(unittest.TestCase):
    def test_raise_inline_raises_runtime_error_when_enabled(self):
        with self.assertRaisesRegex(RuntimeError, "raise_inline exception is raised"):
            raise_inline()

    def test_raise_inline_disable_skips_raising(self):
        self.assertIsNone(raise_inline(disable=True))

    def test_raise_inline_uses_custom_message(self):
        with self.assertRaisesRegex(RuntimeError, "inline custom message"):
            raise_inline(msg="inline custom message")


class TestRaiseRandomDecorator(unittest.TestCase):
    def test_raise_random_rejects_invalid_probability(self):
        with self.assertRaisesRegex(ValueError, "prob_of_raise should be 0-1"):
            raise_random(prob_of_raise=-0.01)

        with self.assertRaisesRegex(ValueError, "prob_of_raise should be 0-1"):
            raise_random(prob_of_raise=1.01)

    def test_raise_random_raises_when_random_value_is_below_threshold(self):
        with patch("fault_injection.raise_exception.random.random", return_value=0.19):
            @raise_random(prob_of_raise=0.2)
            def add(a, b):
                return a + b

            with self.assertRaisesRegex(RuntimeError, "raise_random exception is raised"):
                add(1, 2)

    def test_raise_random_uses_custom_message(self):
        with patch("fault_injection.raise_exception.random.random", return_value=0.1):
            @raise_random(msg="random custom message", prob_of_raise=0.2)
            def add(a, b):
                return a + b

            with self.assertRaisesRegex(RuntimeError, "random custom message"):
                add(1, 2)

    def test_raise_random_calls_wrapped_function_when_random_value_is_above_threshold(self):
        with patch("fault_injection.raise_exception.random.random", return_value=0.9):
            @raise_random(prob_of_raise=0.2)
            def add(a, b):
                return a + b

            self.assertEqual(add(3, 4), 7)

    def test_raise_random_disable_skips_random_and_raising(self):
        with patch(
            "fault_injection.raise_exception.random.random",
            side_effect=AssertionError("random.random should not be called when disabled"),
        ):
            @raise_random(prob_of_raise=1.0, disable=True)
            def add(a, b):
                return a + b

            self.assertEqual(add(10, 5), 15)


class TestRaiseRandomInline(unittest.TestCase):
    def test_raise_random_inline_rejects_invalid_probability(self):
        with self.assertRaisesRegex(ValueError, "prob_of_raise should be 0-1"):
            raise_random_inline(prob_of_raise=-0.01)

        with self.assertRaisesRegex(ValueError, "prob_of_raise should be 0-1"):
            raise_random_inline(prob_of_raise=1.01)

    def test_raise_random_inline_raises_when_random_value_is_below_threshold(self):
        with patch("fault_injection.raise_exception.random.random", return_value=0.19):
            with self.assertRaisesRegex(RuntimeError, "raise_random exception is raised"):
                raise_random_inline(prob_of_raise=0.2)

    def test_raise_random_inline_uses_custom_message(self):
        with patch("fault_injection.raise_exception.random.random", return_value=0.19):
            with self.assertRaisesRegex(RuntimeError, "inline random custom message"):
                raise_random_inline(msg="inline random custom message", prob_of_raise=0.2)

    def test_raise_random_inline_noop_when_random_value_is_above_threshold(self):
        with patch("fault_injection.raise_exception.random.random", return_value=0.9):
            self.assertIsNone(raise_random_inline(prob_of_raise=0.2))

    def test_raise_random_inline_disable_skips_random_and_raising(self):
        with patch(
            "fault_injection.raise_exception.random.random",
            side_effect=AssertionError("random.random should not be called when disabled"),
        ):
            self.assertIsNone(raise_random_inline(prob_of_raise=1.0, disable=True))


class TestRaiseNthDecorator(unittest.TestCase):
    def setUp(self):
        if hasattr(raise_at_nth_call, "n_called_dict"):
            raise_at_nth_call.n_called_dict = {}

    def test_raises_at_n1(self):
        @raise_at_nth_call(n=1, func_id=1)
        def add(a, b):
            return a + b

        with self.assertRaisesRegex(RuntimeError, "raise_at_nth_call exception is raised\nFunc id 1"):
            add(1, 2)

    def test_raise_disable_calls_wrapped_function(self):
        @raise_at_nth_call(n=1, func_id=1, disable=True)
        def add(a, b):
            return a + b

        self.assertEqual(add(2, 3), 5)

    def test_raise_preserves_metadata_with_wraps(self):
        @raise_at_nth_call(n=1, func_id=1, disable=True)
        def add(a, b):
            return a + b

        self.assertEqual(add.__name__, "add")

    def test_raise_uses_custom_message(self):
        @raise_at_nth_call(n=1, func_id=1, msg="custom raise message")
        def add(a, b):
            return a + b

        with self.assertRaisesRegex(RuntimeError, "custom raise message\nFunc id 1"):
            add(1, 2)
    
    def test_raise_at_3rd(self):
        @raise_at_nth_call(n=3, func_id=1, msg="custom raise message")
        def add(a, b):
            return a + b

        add(1, 2)
        add(1, 2)
        with self.assertRaises(RuntimeError):
            add(1, 2)

    def test_explicit_func_id_uses_independent_counters_per_function(self):
        @raise_at_nth_call(n=2, func_id=101)
        def add(a, b):
            return a + b

        @raise_at_nth_call(n=2, func_id=102)
        def mul(a, b):
            return a * b

        self.assertEqual(add(1, 2), 3)
        self.assertEqual(mul(2, 3), 6)
        with self.assertRaisesRegex(RuntimeError, r"\nFunc id 101\Z"):
            add(4, 5)
        with self.assertRaisesRegex(RuntimeError, r"\nFunc id 102\Z"):
            mul(3, 4)

    def test_default_func_id_shares_counter_between_functions(self):
        @raise_at_nth_call(n=2)
        def add(a, b):
            return a + b

        @raise_at_nth_call(n=2)
        def mul(a, b):
            return a * b

        self.assertEqual(add(1, 2), 3)
        with self.assertRaisesRegex(RuntimeError, r"\nFunc id 1\Z"):
            mul(2, 3)
        self.assertEqual(add(4, 5), 9)

    def test_raise_rejects_non_positive_n(self):
        for invalid_n in (0, -1, 1.5):
            with self.subTest(invalid_n=invalid_n):
                with self.assertRaises(ValueError):
                    raise_at_nth_call(n=invalid_n)


class TestRaiseNthInline(unittest.TestCase):
    def setUp(self):
        if hasattr(raise_at_nth_call_inline, "n_called_dict"):
            raise_at_nth_call_inline.n_called_dict = {}

    def test_raises_at_n1(self):
        with self.assertRaisesRegex(RuntimeError, "raise_at_nth_call_inline exception is raised\nFunc id 1"):
            raise_at_nth_call_inline(n=1, func_id=1)

    def test_raise_disable_skips_raising(self):
        self.assertIsNone(raise_at_nth_call_inline(n=1, func_id=1, disable=True))

    def test_raise_uses_custom_message(self):
        with self.assertRaisesRegex(RuntimeError, "inline custom nth message\nFunc id 5"):
            raise_at_nth_call_inline(n=1, func_id=5, msg="inline custom nth message")

    def test_raise_at_3rd(self):
        raise_at_nth_call_inline(n=3, func_id=1)
        raise_at_nth_call_inline(n=3, func_id=1)
        with self.assertRaisesRegex(RuntimeError, "raise_at_nth_call_inline exception is raised\nFunc id 1"):
            raise_at_nth_call_inline(n=3, func_id=1)

    def test_raise_uses_separate_counters_by_func_id(self):
        raise_at_nth_call_inline(n=2, func_id=1)
        raise_at_nth_call_inline(n=2, func_id=2)
        with self.assertRaisesRegex(RuntimeError, "Func id 1"):
            raise_at_nth_call_inline(n=2, func_id=1)
        with self.assertRaisesRegex(RuntimeError, "Func id 2"):
            raise_at_nth_call_inline(n=2, func_id=2)

    def test_explicit_func_id_uses_independent_counters_per_call_site(self):
        def call_first():
            raise_at_nth_call_inline(n=2, func_id=1)

        def call_second():
            raise_at_nth_call_inline(n=2, func_id=2)

        self.assertIsNone(call_first())
        self.assertIsNone(call_second())
        with self.assertRaises(RuntimeError):
            call_first()
        with self.assertRaises(RuntimeError):
            call_second()

    def test_default_func_id_shares_counter_across_call_sites(self):
        def call_first():
            raise_at_nth_call_inline(n=2)

        def call_second():
            raise_at_nth_call_inline(n=2)

        self.assertIsNone(call_first())
        with self.assertRaisesRegex(RuntimeError, r"\nFunc id 1\Z"):
            call_second()
        self.assertIsNone(call_first())

    def test_raise_inline_rejects_non_positive_n(self):
        for invalid_n in (0, -1, 1.5):
            with self.subTest(invalid_n=invalid_n):
                with self.assertRaises(ValueError):
                    raise_at_nth_call_inline(n=invalid_n)

if __name__ == "__main__":
    unittest.main()
