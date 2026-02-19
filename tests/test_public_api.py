import unittest

from src.fault_injection import (
    delay,
    delay_random,
    delay_random_norm,
    raise_,
    raise_random,
)


class TestPublicApi(unittest.TestCase):
    def test_public_api_exports_expected_symbols(self):
        self.assertTrue(callable(delay))
        self.assertTrue(callable(delay_random))
        self.assertTrue(callable(delay_random_norm))
        self.assertTrue(callable(raise_))
        self.assertTrue(callable(raise_random))


if __name__ == "__main__":
    unittest.main()
