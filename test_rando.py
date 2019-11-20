#!/usr/bin/env python

import itertools
import random
import unittest

import rando


def not_so_random(iterable):
    it = itertools.cycle(iterable)

    def rng():
        return next(it)

    return rng


class TestRando(unittest.TestCase):
    seed = 42

    def setUp(self):
        # re-seed the random generator before each test with a constant known value
        # so tests are idempotent
        random.seed(self.seed)
        assert random.random() == 0.6394267984578837

    def test_repr(self):
        weights = [("A", 0.5), ("B", 0.5)]
        rng = rando.Rando(weights, random.random)
        self.assertEqual(
            repr(rng), "Rando([('A', 0.5), ('B', 0.5)], random.random)",
        )

    def test_equal_weights(self):
        weights = [("ITEM_A", 1), ("ITEM_B", 1)]
        rng = rando.Rando(weights, random.random)
        self.assertEqual(
            repr(rng), "Rando([('ITEM_A', 0.5), ('ITEM_B', 0.5)], random.random)",
        )
        self.assertEqual("ITEM_A", next(rng))
        self.assertEqual("ITEM_A", next(rng))
        self.assertEqual("ITEM_A", next(rng))
        self.assertEqual("ITEM_B", next(rng))
        self.assertEqual("ITEM_B", next(rng))
        self.assertEqual("ITEM_B", next(rng))
        self.assertEqual("ITEM_A", next(rng))
        self.assertEqual("ITEM_A", next(rng))
        self.assertEqual("ITEM_A", next(rng))
        self.assertEqual("ITEM_A", next(rng))

    def test_custom_generator(self):
        weights = [("ITEM_A", 1), ("ITEM_B", 1)]
        rng = rando.Rando(weights, not_so_random([0.25, 0.75]))
        self.assertEqual("ITEM_A", next(rng))
        self.assertEqual("ITEM_B", next(rng))
        self.assertEqual("ITEM_A", next(rng))
        self.assertEqual("ITEM_B", next(rng))
        self.assertEqual("ITEM_A", next(rng))
        self.assertEqual("ITEM_B", next(rng))
        self.assertEqual("ITEM_A", next(rng))
        self.assertEqual("ITEM_B", next(rng))
        self.assertEqual("ITEM_A", next(rng))
        self.assertEqual("ITEM_B", next(rng))


if __name__ == "__main__":
    unittest.main()
