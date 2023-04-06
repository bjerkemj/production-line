import unittest
import os
import sys
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT+"/..")
from batch import Batch, batchGenerator

class TestBatch(unittest.TestCase):

    def test_init(self):
        batch = Batch("1", 20)
        self.assertEqual(batch.batchNumber, "1")
        self.assertEqual(batch.batchSize, 20)
        self.assertEqual(batch.prevTask, 0)
        self.assertEqual(batch.prevBuffer, 0)
        self.assertEqual(batch.location, "Start")

    def test_repr(self):
        batch = Batch("1", 20)
        self.assertEqual(repr(batch), "Batch 1 of size 20")

    def test_getBatchSize(self):
        batch = Batch("1", 20)
        self.assertEqual(batch.getBatchSize(), 20)

    def test_getBatchNumber(self):
        batch = Batch("1", 20)
        self.assertEqual(batch.getBatchNumber(), "1")

    def test_getLocation(self):
        batch = Batch("1", 20)
        self.assertEqual(batch.getLocation(), "Start")

    def test_setLocation(self):
        batch = Batch("1", 20)
        batch.setLocation("Processing")
        self.assertEqual(batch.getLocation(), "Processing")

class TestBatchGenerator(unittest.TestCase):

    def test_batchGenerator(self):
        generator = batchGenerator()
        first_batch = next(generator)
        second_batch = next(generator)

        self.assertIsInstance(first_batch, Batch)
        self.assertIsInstance(second_batch, Batch)
        self.assertEqual(first_batch.getBatchNumber(), "1")
        self.assertEqual(first_batch.getBatchSize(), 20)
        self.assertEqual(second_batch.getBatchNumber(), "2")
        self.assertEqual(second_batch.getBatchSize(), 20)

if __name__ == "__main__":
    unittest.main()