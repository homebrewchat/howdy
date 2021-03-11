import unittest

from hbcbot import commands


class TestAbv(unittest.TestCase):
    def test_pastryboi(self):
        abv = commands._abv(1.135, 1.045)
        abv = round(abv, 1)
        self.assertEqual(abv, 14.1)


class TestBrix(unittest.TestCase):
    def test_brix(self):
        brix = commands._brix_to_og(31.2)
        brix = round(brix, 3)
        self.assertEqual(brix, 1.135)


class TestHydrometer(unittest.TestCase):
    def test_hyadj(self):
        ag = commands._hydro_temp_adj(1.131, 90, 60)
        ag = round(ag, 3)
        self.assertEqual(ag, 1.135)
