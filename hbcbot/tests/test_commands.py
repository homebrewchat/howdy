import unittest

from hbcbot import commands


class TestAbv(unittest.TestCase):
    def test_pastryboi(self):
        abv = commands._abv(1.135, 1.045)
        abv = round(abv, 1)
        self.assertEqual(abv, 14.1)
