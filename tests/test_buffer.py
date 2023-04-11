import unittest
import os
import sys
import io
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT+"/..")
from batch import Batch
from buffer import Buffer
from unittest.mock import patch, MagicMock

class TestBuffer(unittest.TestCase):
    def setUp(self):
        self.old_stdout = sys.stdout
        sys.stdout = self.buffer = io.StringIO()

    def tearDown(self) -> None:
        sys.stdout = self.old_stdout

    def test_init(self):
        with patch('eventManager.EventQueue') as EventQueue:
            mock_eq = EventQueue.return_value
            buffer = Buffer("0", mock_eq)

            self.assertEqual(buffer.bufferNumber, "0")
            self.assertEqual(buffer.capacity, 120)
            self.assertEqual(buffer.numberOfWafersInBuffer, 0)
            self.assertEqual(buffer.reservedSpace, 0)
            self.assertFalse(buffer.isFinalBuffer)
            self.assertFalse(buffer.isFirstBuffer)
            self.assertIsNone(buffer.nextTask)
            self.assertIsNone(buffer.prevTask)
            self.assertIsNone(buffer.productionLine)
    
    def test_repr(self):
        with patch('eventManager.EventQueue') as EventQueue:
            mock_eq = EventQueue.return_value
            buffer = Buffer("0", mock_eq)

            self.assertEqual(repr(buffer), "Buffer 0")

    def test_load_and_unload_batch(self):
        with patch('eventManager.EventQueue') as EventQueue:
            mock_eq = EventQueue.return_value
            buffer = Buffer("0", mock_eq, isFinalBuffer=True)
            batch1 = Batch("0", 20)

            buffer.loadBatchToBuffer(0, batch1)

            self.assertEqual(len(buffer.getBatches()), 1)
            self.assertEqual(buffer.getNumberOfWafersInBuffer(), batch1.getBatchSize())

            unloaded_batch = buffer.unloadOldestBatchFromBuffer(0)
            self.assertEqual(unloaded_batch, batch1)
            self.assertEqual(len(buffer.getBatches()), 0)
            self.assertEqual(buffer.getNumberOfWafersInBuffer(), 0)

    def test_reserve_space(self):
        with patch('eventManager.EventQueue') as EventQueue:
            mock_eq = EventQueue.return_value
            buffer = Buffer("0", mock_eq)
            buffer.reserveSpace(30)

            self.assertEqual(buffer.reservedSpace, 30)

    def test_can_add_batch(self):
        with patch('eventManager.EventQueue') as EventQueue:
            mock_eq = EventQueue.return_value
            buffer = Buffer("0", mock_eq)
            batch1 = Batch("1", 20)

            self.assertTrue(buffer.canAddBatch(batch1))

            buffer.capacity = 10
            self.assertFalse(buffer.canAddBatch(batch1))

    def test_has_batch_ready_to_process(self):
        with patch('eventManager.EventQueue') as EventQueue:
            mock_eq = EventQueue.return_value
            buffer = Buffer("0", mock_eq)
            batch1 = Batch("0", 20)
            self.assertFalse(buffer.hasBatchReadyToProcess())

            mock_next_task = MagicMock()
            buffer.setNextTask(mock_next_task)

            buffer.loadBatchToBuffer(0, batch1)
            self.assertTrue(buffer.hasBatchReadyToProcess())


if __name__ == "__main__":
    unittest.main()