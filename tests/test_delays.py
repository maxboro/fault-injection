import unittest
from unittest.mock import patch

from src.fault_injection import (
    delay,
    delay_inline,
    delay_random,
    delay_random_inline,
    delay_random_norm,
    delay_random_norm_inline,
    delay_at_nth_call,
    delay_at_nth_call_inline
)


class TestDelayDecorator(unittest.TestCase):
    def test_delay_rejects_negative_time(self):
        with self.assertRaisesRegex(ValueError, "delay should have positive time_s"):
            delay(-0.1)

    def test_delay_calls_sleep_and_returns_wrapped_value(self):
        with patch("src.fault_injection.delays.time.sleep") as sleep_mock:
            @delay(0.25)
            def add(a, b):
                return a + b

            self.assertEqual(add(1, 3), 4)
            sleep_mock.assert_called_once_with(0.25)

    def test_delay_disable_skips_sleep(self):
        with patch(
            "src.fault_injection.delays.time.sleep",
            side_effect=AssertionError("time.sleep should not be called when disabled"),
        ):
            @delay(0.25, disable=True)
            def add(a, b):
                return a + b

            self.assertEqual(add(2, 5), 7)


class TestDelayInline(unittest.TestCase):
    def test_delay_inline_rejects_negative_time(self):
        with self.assertRaisesRegex(ValueError, "delay should have positive time_s"):
            delay_inline(-0.1)

    def test_delay_inline_calls_sleep(self):
        with patch("src.fault_injection.delays.time.sleep") as sleep_mock:
            self.assertIsNone(delay_inline(0.25))
            sleep_mock.assert_called_once_with(0.25)

    def test_delay_inline_disable_skips_sleep(self):
        with patch(
            "src.fault_injection.delays.time.sleep",
            side_effect=AssertionError("time.sleep should not be called when disabled"),
        ):
            self.assertIsNone(delay_inline(0.25, disable=True))


class TestDelayRandomDecorator(unittest.TestCase):
    def test_delay_random_rejects_negative_max_time(self):
        with self.assertRaisesRegex(ValueError, "delay_random should have positive max_time_s"):
            delay_random(-0.1)

    def test_delay_random_uses_randomized_delay(self):
        with patch("src.fault_injection.delays.random.random", return_value=0.5):
            with patch("src.fault_injection.delays.time.sleep") as sleep_mock:
                @delay_random(0.4)
                def add(a, b):
                    return a + b

                self.assertEqual(add(4, 6), 10)
                sleep_mock.assert_called_once_with(0.2)

    def test_delay_random_disable_skips_random_and_sleep(self):
        with patch(
            "src.fault_injection.delays.random.random",
            side_effect=AssertionError("random.random should not be called when disabled"),
        ):
            with patch(
                "src.fault_injection.delays.time.sleep",
                side_effect=AssertionError("time.sleep should not be called when disabled"),
            ):
                @delay_random(0.4, disable=True)
                def add(a, b):
                    return a + b

                self.assertEqual(add(5, 6), 11)


class TestDelayRandomInline(unittest.TestCase):
    def test_delay_random_inline_rejects_negative_max_time(self):
        with self.assertRaisesRegex(ValueError, "delay_random_inline should have positive max_time_s"):
            delay_random_inline(-0.1)

    def test_delay_random_inline_uses_randomized_delay(self):
        with patch("src.fault_injection.delays.random.random", return_value=0.5):
            with patch("src.fault_injection.delays.time.sleep") as sleep_mock:
                self.assertIsNone(delay_random_inline(0.4))
                sleep_mock.assert_called_once_with(0.2)

    def test_delay_random_inline_disable_skips_random_and_sleep(self):
        with patch(
            "src.fault_injection.delays.random.random",
            side_effect=AssertionError("random.random should not be called when disabled"),
        ):
            with patch(
                "src.fault_injection.delays.time.sleep",
                side_effect=AssertionError("time.sleep should not be called when disabled"),
            ):
                self.assertIsNone(delay_random_inline(0.4, disable=True))


class TestDelayRandomNormDecorator(unittest.TestCase):
    def test_delay_random_norm_rejects_negative_parameters(self):
        with self.assertRaisesRegex(ValueError, "delay_random_norm should have positive mean_time_s"):
            delay_random_norm(mean_time_s=-0.1, std_time_s=0.1)

        with self.assertRaisesRegex(ValueError, "delay_random_norm should have positive std_time_s"):
            delay_random_norm(mean_time_s=0.1, std_time_s=-0.1)

    def test_delay_random_norm_uses_gaussian_value_when_positive(self):
        with patch("src.fault_injection.delays.random.gauss", return_value=0.35):
            with patch("src.fault_injection.delays.time.sleep") as sleep_mock:
                @delay_random_norm(mean_time_s=0.3, std_time_s=0.1)
                def add(a, b):
                    return a + b

                self.assertEqual(add(7, 8), 15)
                sleep_mock.assert_called_once_with(0.35)

    def test_delay_random_norm_clamps_negative_gaussian_value_to_zero(self):
        with patch("src.fault_injection.delays.random.gauss", return_value=-0.7):
            with patch("src.fault_injection.delays.time.sleep") as sleep_mock:
                @delay_random_norm(mean_time_s=0.3, std_time_s=0.1)
                def add(a, b):
                    return a + b

                self.assertEqual(add(7, 8), 15)
                sleep_mock.assert_called_once_with(0)

    def test_delay_random_norm_disable_skips_gauss_and_sleep(self):
        with patch(
            "src.fault_injection.delays.random.gauss",
            side_effect=AssertionError("random.gauss should not be called when disabled"),
        ):
            with patch(
                "src.fault_injection.delays.time.sleep",
                side_effect=AssertionError("time.sleep should not be called when disabled"),
            ):
                @delay_random_norm(mean_time_s=0.3, std_time_s=0.1, disable=True)
                def add(a, b):
                    return a + b

                self.assertEqual(add(9, 1), 10)


class TestDelayRandomNormInline(unittest.TestCase):
    def test_delay_random_norm_inline_rejects_negative_parameters(self):
        with self.assertRaisesRegex(ValueError, "delay_random_norm should have positive mean_time_s"):
            delay_random_norm_inline(mean_time_s=-0.1, std_time_s=0.1)

        with self.assertRaisesRegex(ValueError, "delay_random_norm should have positive std_time_s"):
            delay_random_norm_inline(mean_time_s=0.1, std_time_s=-0.1)

    def test_delay_random_norm_inline_uses_gaussian_value_when_positive(self):
        with patch("src.fault_injection.delays.random.gauss", return_value=0.35):
            with patch("src.fault_injection.delays.time.sleep") as sleep_mock:
                self.assertIsNone(delay_random_norm_inline(mean_time_s=0.3, std_time_s=0.1))
                sleep_mock.assert_called_once_with(0.35)

    def test_delay_random_norm_inline_clamps_negative_gaussian_value_to_zero(self):
        with patch("src.fault_injection.delays.random.gauss", return_value=-0.7):
            with patch("src.fault_injection.delays.time.sleep") as sleep_mock:
                self.assertIsNone(delay_random_norm_inline(mean_time_s=0.3, std_time_s=0.1))
                sleep_mock.assert_called_once_with(0)

    def test_delay_random_norm_inline_disable_skips_gauss_and_sleep(self):
        with patch(
            "src.fault_injection.delays.random.gauss",
            side_effect=AssertionError("random.gauss should not be called when disabled"),
        ):
            with patch(
                "src.fault_injection.delays.time.sleep",
                side_effect=AssertionError("time.sleep should not be called when disabled"),
            ):
                self.assertIsNone(
                    delay_random_norm_inline(mean_time_s=0.3, std_time_s=0.1, disable=True)
                )


class TestDelayNthDecorator(unittest.TestCase):
    def setUp(self):
        if hasattr(delay_at_nth_call, "n_called_dict"):
            delay_at_nth_call.n_called_dict = {}

    def test_delay_at_n1_calls_sleep_and_returns_wrapped_value(self):
        with patch("src.fault_injection.delays.time.sleep") as sleep_mock:
            @delay_at_nth_call(time_s=0.25, n=1, func_id=1)
            def add(a, b):
                return a + b

            self.assertEqual(add(1, 2), 3)
            sleep_mock.assert_called_once_with(0.25)

    def test_delay_disable_skips_sleep(self):
        with patch(
            "src.fault_injection.delays.time.sleep",
            side_effect=AssertionError("time.sleep should not be called when disabled"),
        ):
            @delay_at_nth_call(time_s=0.25, n=1, func_id=1, disable=True)
            def add(a, b):
                return a + b

            self.assertEqual(add(2, 3), 5)

    def test_delay_preserves_metadata_with_wraps(self):
        @delay_at_nth_call(time_s=0.25, n=1, func_id=1, disable=True)
        def add(a, b):
            return a + b

        self.assertEqual(add.__name__, "add")

    def test_delay_at_3rd_call(self):
        with patch("src.fault_injection.delays.time.sleep") as sleep_mock:
            @delay_at_nth_call(time_s=0.25, n=3, func_id=1)
            def add(a, b):
                return a + b

            self.assertEqual(add(1, 2), 3)
            self.assertEqual(add(1, 2), 3)
            self.assertEqual(add(1, 2), 3)
            self.assertEqual(add(1, 2), 3)
            sleep_mock.assert_called_once_with(0.25)

    def test_explicit_func_id_uses_independent_counters_per_function(self):
        with patch("src.fault_injection.delays.time.sleep") as sleep_mock:
            @delay_at_nth_call(time_s=0.4, n=2, func_id=101)
            def add(a, b):
                return a + b

            @delay_at_nth_call(time_s=0.4, n=2, func_id=102)
            def mul(a, b):
                return a * b

            self.assertEqual(add(1, 2), 3)
            self.assertEqual(mul(2, 3), 6)
            self.assertEqual(add(4, 5), 9)
            self.assertEqual(mul(3, 4), 12)
            self.assertEqual(sleep_mock.call_count, 2)

    def test_default_func_id_shares_counter_between_functions(self):
        with patch("src.fault_injection.delays.time.sleep") as sleep_mock:
            @delay_at_nth_call(time_s=0.4, n=2)
            def add(a, b):
                return a + b

            @delay_at_nth_call(time_s=0.4, n=2)
            def mul(a, b):
                return a * b

            self.assertEqual(add(1, 2), 3)
            self.assertEqual(mul(2, 3), 6)
            self.assertEqual(add(4, 5), 9)
            sleep_mock.assert_called_once_with(0.4)

    def test_delay_rejects_non_positive_n(self):
        for invalid_n in (0, -1, 1.5):
            with self.subTest(invalid_n=invalid_n):
                with self.assertRaises(ValueError):
                    delay_at_nth_call(n=invalid_n)

    def test_delay_rejects_negative_time(self):
        with self.assertRaisesRegex(ValueError, "delay should have positive time_s"):
            delay_at_nth_call(time_s=-0.1)


class TestDelayNthInline(unittest.TestCase):
    def setUp(self):
        if hasattr(delay_at_nth_call_inline, "n_called_dict"):
            delay_at_nth_call_inline.n_called_dict = {}

    def test_delay_at_n1_calls_sleep(self):
        with patch("src.fault_injection.delays.time.sleep") as sleep_mock:
            self.assertIsNone(delay_at_nth_call_inline(time_s=0.25, n=1, func_id=1))
            sleep_mock.assert_called_once_with(0.25)

    def test_delay_disable_skips_sleep(self):
        with patch(
            "src.fault_injection.delays.time.sleep",
            side_effect=AssertionError("time.sleep should not be called when disabled"),
        ):
            self.assertIsNone(delay_at_nth_call_inline(time_s=0.25, n=1, func_id=1, disable=True))

    def test_delay_at_3rd_call(self):
        with patch("src.fault_injection.delays.time.sleep") as sleep_mock:
            self.assertIsNone(delay_at_nth_call_inline(time_s=0.25, n=3, func_id=1))
            self.assertIsNone(delay_at_nth_call_inline(time_s=0.25, n=3, func_id=1))
            self.assertIsNone(delay_at_nth_call_inline(time_s=0.25, n=3, func_id=1))
            self.assertIsNone(delay_at_nth_call_inline(time_s=0.25, n=3, func_id=1))
            sleep_mock.assert_called_once_with(0.25)

    def test_explicit_func_id_uses_independent_counters_per_call_site(self):
        with patch("src.fault_injection.delays.time.sleep") as sleep_mock:
            def call_first():
                delay_at_nth_call_inline(time_s=0.4, n=2, func_id=1)

            def call_second():
                delay_at_nth_call_inline(time_s=0.4, n=2, func_id=2)

            self.assertIsNone(call_first())
            self.assertIsNone(call_second())
            self.assertIsNone(call_first())
            self.assertIsNone(call_second())
            self.assertEqual(sleep_mock.call_count, 2)

    def test_default_func_id_shares_counter_across_call_sites(self):
        with patch("src.fault_injection.delays.time.sleep") as sleep_mock:
            def call_first():
                delay_at_nth_call_inline(time_s=0.4, n=2)

            def call_second():
                delay_at_nth_call_inline(time_s=0.4, n=2)

            self.assertIsNone(call_first())
            self.assertIsNone(call_second())
            self.assertIsNone(call_first())
            sleep_mock.assert_called_once_with(0.4)

    def test_delay_inline_rejects_non_positive_n(self):
        for invalid_n in (0, -1, 1.5):
            with self.subTest(invalid_n=invalid_n):
                with self.assertRaises(ValueError):
                    delay_at_nth_call_inline(n=invalid_n)

    def test_delay_inline_rejects_negative_time(self):
        with self.assertRaisesRegex(ValueError, "delay should have positive time_s"):
            delay_at_nth_call_inline(time_s=-0.1)


if __name__ == "__main__":
    unittest.main()
