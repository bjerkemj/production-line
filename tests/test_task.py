import unittest
import os
import sys
import io
from unittest.mock import MagicMock, patch
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT+"/..")

from task import Task

class TestEvent(unittest.TestCase):
    def setUp(self):
        self.mock_buffer1 = MagicMock()
        self.mock_buffer2 = MagicMock()
        self.mock_buffer1.bufferNumber = "1"
        self.mock_buffer2.bufferNumber = "2"

    def test_init(self):
        task = Task("1", self.mock_buffer1, self.mock_buffer2, None)

        self.assertEqual(task.taskNumber, "1")
        self.assertEqual(task.inputBuffer.bufferNumber, "1")
        self.assertEqual(task.outputBuffer.bufferNumber, "2")
        self.assertEqual(task.eventQueue, None)

    def test_repr(self):
        task = Task("1", self.mock_buffer1, self.mock_buffer2, None)
        self.assertEqual(repr(task), "Task 1")

    def test_set_unit(self):
        with patch('unit.Unit') as Unit:
            mock_unit = Unit.return_value
            task = Task("1", self.mock_buffer1, self.mock_buffer2, None)
            task.setUnit(mock_unit)
            self.assertEqual(task.unit, mock_unit)

    def test_get_set_buffer(self):
        task = Task("1", self.mock_buffer1, self.mock_buffer2, None)

        mock_buffer3 = MagicMock()
        mock_buffer4 = MagicMock()
        mock_buffer3.bufferNumber = "3"
        mock_buffer4.bufferNumber = "4"

        task.setInputBuffer(mock_buffer3)
        task.setOutputBuffer(mock_buffer4)

        self.assertEqual(task.getInputBuffer().bufferNumber, "3")
        self.assertEqual(task.getOutputBuffer().bufferNumber, "4")

    def test_batch_ready_to_process(self):
        self.mock_buffer1.hasBatchReadyToProcess.return_value = True
        mock_oldest_batch = MagicMock()
        self.mock_buffer1.getOldestBatchFromBuffer.return_value = mock_oldest_batch

        self.mock_buffer2.canAddBatch.return_value = True

        task = Task("1", self.mock_buffer1, self.mock_buffer2, None)

        self.assertTrue(task.hasBatchReadyToProcess())

    def test_notify_buffer(self):
        task = Task("1", self.mock_buffer1, self.mock_buffer2, None)
        with patch('unit.Unit') as Unit:
            mock_unit = Unit.return_value
            mock_unit.notifyTaskIsInQueue = MagicMock()
            task.setUnit(mock_unit)

            task.notifyBufferIsInQueue(5)

            mock_unit.notifyTaskIsInQueue.assert_called_once_with(5)

    def test_process_next_batch_not_possible(self):
        self.mock_buffer1.hasBatchReadyToProcess.return_value = False
        task = Task("1", self.mock_buffer1, self.mock_buffer2, None)

        self.old_stdout = sys.stdout
        sys.stdout = self.buffer = io.StringIO()

        task.processNextBatch(5)
        log = self.buffer.getvalue()

        self.assertEqual(log, "No batches to process\n")

        sys.stdout = self.old_stdout

    def test_process_next_batch_not_possible(self):
        self.mock_buffer1.hasBatchReadyToProcess.return_value = True
        mock_oldest_batch = MagicMock()
        self.mock_buffer1.getOldestBatchFromBuffer.return_value = mock_oldest_batch
        self.mock_buffer2.canAddBatch.return_value = True

        with patch('eventManager.EventQueue') as EventQueue:
            with patch('unit.Unit') as Unit:
                mock_unit = Unit.return_value
                mock_unit.setIdleToTrue = MagicMock()
                mock_eq = EventQueue.return_value
                mock_eq.createAndQueueEvent = MagicMock()
                task = Task("1", self.mock_buffer1, self.mock_buffer2, mock_eq)
                task.setUnit(mock_unit)

                self.old_stdout = sys.stdout
                sys.stdout = self.buffer = io.StringIO()

                task.processNextBatch(5)
                log = self.buffer.getvalue()

                self.assertTrue(log)

                sys.stdout = self.old_stdout

                mock_eq.createAndQueueEvent.assert_called()


if __name__ == "__main__":
    unittest.main()