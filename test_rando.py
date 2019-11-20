#!/usr/bin/env python

import itertools
import random
import unittest

import rando


class NotSoRandom(object):
    def __init__(self, iterable):
        self.iterator = itertools.cycle(iterable)

    def __repr__(self):
        return "NotSoRandom"

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.iterator)

    __call__ = __next__
    next = __next__


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

    def test_inequal_weights(self):
        weights = [("ITEM_A", 1), ("ITEM_B", 1), ("ITEM_C", 2)]
        rng = rando.Rando(weights, random.random)
        self.assertEqual(
            repr(rng),
            "Rando([('ITEM_A', 0.25), ('ITEM_B', 0.25), ('ITEM_C', 0.5)], random.random)",
        )
        self.assertEqual("ITEM_A", next(rng))
        self.assertEqual("ITEM_B", next(rng))
        self.assertEqual("ITEM_A", next(rng))
        self.assertEqual("ITEM_C", next(rng))
        self.assertEqual("ITEM_C", next(rng))
        self.assertEqual("ITEM_C", next(rng))
        self.assertEqual("ITEM_A", next(rng))
        self.assertEqual("ITEM_B", next(rng))
        self.assertEqual("ITEM_A", next(rng))
        self.assertEqual("ITEM_A", next(rng))

    def test_custom_generator(self):
        weights = [("ITEM_A", 1), ("ITEM_B", 1)]
        rng = rando.Rando(weights, NotSoRandom([0.25, 0.75]))
        self.assertEqual(
            repr(rng), "Rando([('ITEM_A', 0.5), ('ITEM_B', 0.5)], NotSoRandom)"
        )
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

    def test_invalid_generator(self):
        weights = [("ITEM_A", 1), ("ITEM_B", 1)]
        rng = rando.Rando(weights, NotSoRandom([1]))
        self.assertEqual(
            repr(rng), "Rando([('ITEM_A', 0.5), ('ITEM_B', 0.5)], NotSoRandom)"
        )
        with self.assertRaises(RuntimeError):
            next(rng)


if __name__ == "__main__":
    unittest.main()
