import unittest
import os
import sys
import io
from unittest.mock import patch
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT+"/..")
from productionLine import ProductionLine

class TestBuffer(unittest.TestCase):
    def test_init(self):
        with patch('eventManager.EventQueue') as EventQueue:
            mock_eq = EventQueue.return_value
        pl = ProductionLine(mock_eq)

        self.assertEqual(len(pl.buffers), 10)
        self.assertEqual(len(pl.tasks), 9)
        self.assertEqual(len(pl.units), 3)
        self.assertEqual(pl.eventQueue, mock_eq)

    def test_load_batch_to_production_line(self):
        pl = ProductionLine(None)

        with patch.object(pl.buffers[0], 'canAddBatch') as mock_can_add_batch, \
             patch.object(pl.buffers[0], 'reserveSpace') as mock_reserve_space, \
             patch.object(pl.buffers[0], 'loadBatchToBuffer') as mock_load_batch_to_buffer, \
            patch('batch.Batch') as Batch:

            batch = Batch.return_value
            mock_can_add_batch.return_value = True

            pl.loadBatchToProductionLine(0, batch)

            mock_can_add_batch.assert_called_once_with(batch)
            mock_reserve_space.assert_called_once_with(batch.getBatchSize())
            mock_load_batch_to_buffer.assert_called_once_with(0, batch)

    def test_load_batch_to_production_line_fail(self):
        import types

        eq = types.SimpleNamespace()
        eq.createAndQueueEvent = None
        pl = ProductionLine(eq)

        with patch.object(pl.buffers[0], 'canAddBatch') as mock_can_add_batch, \
             patch.object(eq, 'createAndQueueEvent') as mock_create_and_queue_event, \
             patch('batch.Batch') as Batch:
            
            batch = Batch.return_value
            mock_can_add_batch.return_value = False

            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()

            pl.loadBatchToProductionLine(0, batch)

            log = buffer.getvalue()
            sys.stdout = old_stdout

            mock_can_add_batch.assert_called_once_with(batch)
            mock_create_and_queue_event.assert_called_once_with(1, pl, pl.loadBatchToProductionLine, batch)
            self.assertEqual(log, "Couldn't load batch, trying again at time 50\n")

if __name__ == "__main__":
    unittest.main()