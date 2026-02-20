import unittest

from fault_injection import (
    delay,
    delay_at_nth_call,
    delay_at_nth_call_inline,
    delay_inline,
    delay_random,
    delay_random_inline,
    delay_random_norm,
    delay_random_norm_inline,
    raise_,
    raise_at_nth_call,
    raise_at_nth_call_inline,
    raise_inline,
    raise_random,
    raise_random_inline,
)


class TestPublicApi(unittest.TestCase):
    def test_public_api_exports_expected_symbols(self):
        self.assertTrue(callable(delay))
        self.assertTrue(callable(delay_at_nth_call))
        self.assertTrue(callable(delay_at_nth_call_inline))
        self.assertTrue(callable(delay_inline))
        self.assertTrue(callable(delay_random))
        self.assertTrue(callable(delay_random_inline))
        self.assertTrue(callable(delay_random_norm))
        self.assertTrue(callable(delay_random_norm_inline))
        self.assertTrue(callable(raise_))
        self.assertTrue(callable(raise_at_nth_call))
        self.assertTrue(callable(raise_at_nth_call_inline))
        self.assertTrue(callable(raise_inline))
        self.assertTrue(callable(raise_random))
        self.assertTrue(callable(raise_random_inline))


if __name__ == "__main__":
    unittest.main()
