import unittest
import os
import sys
import io
from unittest.mock import MagicMock, patch
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT+"/..")
from unit import Unit


class TestBuffer(unittest.TestCase):
    def test_init(self):
        unit0 = Unit("1", None, [])

        self.assertEqual(unit0.unitNumber, "1")
        self.assertEqual(unit0.tasks, [])
        self.assertTrue(unit0.idle)
    
    def test_repr(self):
        unit = Unit("1", None, [])
        self.assertEqual(repr(unit), "Unit 1")

    def test_add_task(self):
        with patch("task.Task") as Task:
            mock_task = Task.return_value
            unit = Unit("1", None, [])

            unit.addTask(mock_task)
            self.assertEqual(len(unit.tasks), 1)

    def test_notify_task(self):
        with patch('eventManager.EventQueue') as EventQueue:
            mock_eq = EventQueue.return_value
            mock_eq.createAndQueueEvent = MagicMock()

            unit = Unit("1", mock_eq, [])
            unit.notifyTaskIsInQueue(5)

            mock_eq.createAndQueueEvent.assert_called_once()

    def test_set_idle_to_true(self):
        with patch('eventManager.EventQueue') as EventQueue:
            mock_eq = EventQueue.return_value
            mock_eq.createAndQueueEvent = MagicMock()
            
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()

            unit = Unit("1", mock_eq, [])
            unit.setIdleToTrue(5)

            log = buffer.getvalue()
            sys.stdout = old_stdout
            
            
            self.assertEqual(log, "Unit 1 is set idle to true at 5\n")
            self.assertTrue(unit.idle)
            mock_eq.createAndQueueEvent.assert_called_once()

    def test_process_next_batch_fail(self):
        unit = Unit("1", None, [])
        unit.idle = False

        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()

        unit.processNextBatch(5)

        log = buffer.getvalue()
        sys.stdout = old_stdout

        self.assertEqual(log, "Unit 1 is not idle. Cannot process at current time.\n")

    def test_process_next_batch(self):
        with patch("task.Task") as Task:
            mock_task = Task.return_value
            mock_task.hasBatchReadyToProcess.return_value = True
            mock_task.processNextBatch = MagicMock()

            unit = Unit("1", None, [])

            unit.addTask(mock_task)

            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()

            unit.processNextBatch(5)

            log = buffer.getvalue()
            sys.stdout = old_stdout


            self.assertEqual(log, "Unit 1 is processing a batch at time 5\n")
            self.assertFalse(unit.idle)
            mock_task.processNextBatch.assert_called_once()
    
if __name__ == "__main__":
    unittest.main()