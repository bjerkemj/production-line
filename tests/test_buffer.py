import unittest
import os
import sys
import io
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT+"/..")
from eventManager import EventQueue
from batch import batchGenerator
from buffer import Buffer

class TestBuffer(unittest.TestCase):
    def test_init_and_repr(self):
        eq = EventQueue()
        buffer = Buffer("0", eq)

        self.assertEqual(buffer.bufferNumber, "0")
        self.assertEqual(buffer.capacity, 120)
        self.assertEqual(buffer.numberOfWafersInBuffer, 0)
        self.assertEqual(buffer.reservedSpace, 0)
        self.assertFalse(buffer.isFinalBuffer)
        self.assertFalse(buffer.isFirstBuffer)
        self.assertIsNone(buffer.nextTask)
        self.assertIsNone(buffer.prevTask)
        self.assertIsNone(buffer.productionLine)
        self.assertEqual(repr(buffer), "Buffer 0")

    def test_load_and_unload_batch(self):
        eq = EventQueue()
        buffer = Buffer("0", eq, isFinalBuffer=True)
        batch_gen = batchGenerator()
        batch1 = next(batch_gen)

        buffer.loadBatchToBuffer(0, batch1)

        self.assertEqual(len(buffer.getBatches()), 1)
        self.assertEqual(buffer.getNumberOfWafersInBuffer(), batch1.getBatchSize())

        unloaded_batch = buffer.unloadOldestBatchFromBuffer(0)
        self.assertEqual(unloaded_batch, batch1)
        self.assertEqual(len(buffer.getBatches()), 0)
        self.assertEqual(buffer.getNumberOfWafersInBuffer(), 0)

    def test_reserve_space(self):
        eq = EventQueue()
        buffer = Buffer("0", eq)
        buffer.reserveSpace(30)

        self.assertEqual(buffer.reservedSpace, 30)

    def test_can_add_batch(self):
        eq = EventQueue()
        buffer = Buffer("0", eq)
        batch_gen = batchGenerator()
        batch1 = next(batch_gen)

        self.assertTrue(buffer.canAddBatch(batch1))

        buffer.capacity = 10
        self.assertFalse(buffer.canAddBatch(batch1))

    def test_has_batch_ready_to_process(self):
        eq = EventQueue()
        buffer = Buffer("0", eq, isFinalBuffer=True)
        batch_gen = batchGenerator()
        batch1 = next(batch_gen)

        self.assertFalse(buffer.hasBatchReadyToProcess())

        buffer.loadBatchToBuffer(0, batch1)
        self.assertTrue(buffer.hasBatchReadyToProcess())

if __name__ == "__main__":
    unittest.main()