import unittest
import os
import sys
import io
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT+"/..")
from eventManager import TestObject, Event, EventQueue

class TestEvent(unittest.TestCase):
    def setUp(self):
        self.old_stdout = sys.stdout
        sys.stdout = self.buffer = io.StringIO()

    def tearDown(self) -> None:
        sys.stdout = self.old_stdout

    def test_init_and_execute_event(self):
        test_obj = TestObject()
        event = Event(5, test_obj, test_obj.fun, "parameter 1", "parameter 2")

        self.assertEqual(event.time, 5)
        self.assertEqual(event.object, test_obj)
        self.assertEqual(event.function, test_obj.fun)
        self.assertEqual(event.functionParameters, ("parameter 1", "parameter 2"))
        
        event.executeEvent()

        log = self.buffer.getvalue()
        
        expected_logs = "time is 5\nparameter 1 parameter 2\n"
        self.assertEqual(log, expected_logs)

    def test_repr(self):
        test_obj = TestObject()
        event = Event(5, test_obj, test_obj.fun, "parameter 1", "parameter 2")
        self.assertEqual(repr(event), "Event at time 5 on object <eventManager.TestObject object at ADDRESS> is function fun with args ('parameter 1', 'parameter 2')".replace("ADDRESS", hex(id(test_obj))))

class TestEventQueue(unittest.TestCase):
    def setUp(self):
        self.old_stdout = sys.stdout
        sys.stdout = self.buffer = io.StringIO()

    def tearDown(self) -> None:
        sys.stdout = self.old_stdout

    def test_init(self):
        eq = EventQueue()
        self.assertEqual(eq.time, 0)
        self.assertEqual(eq.eventset, [])
        self.assertEqual(eq.oldEvents, [])

    def test_queue_event(self):
        eq = EventQueue()
        test_obj = TestObject()
        event1 = Event(1, test_obj, test_obj.fun, "parameter 1", "parameter 2")
        event2 = Event(2, test_obj, test_obj.fun, "parameter 3", "parameter 4")

        eq.queueEvent(event1)
        eq.queueEvent(event2)

        self.assertEqual(eq.eventset, [event1, event2])

    def test_is_empty(self):
        eq = EventQueue()
        self.assertTrue(eq.isEmpty())

    def test_create_and_queue_event(self):
        eq = EventQueue()
        test_obj = TestObject()

        eq.createAndQueueEvent(3, test_obj, test_obj.fun, "parameter 1", "parameter 2")
        event = eq.eventset[0]

        self.assertEqual(event.time, 3)
        self.assertEqual(event.object, test_obj)
        self.assertEqual(event.function, test_obj.fun)
        self.assertEqual(event.functionParameters, ("parameter 1", "parameter 2"))

    def test_has_next_event(self):
        eq = EventQueue()
        test_obj = TestObject()
        self.assertFalse(eq.hasNextEvent())

        eq.createAndQueueEvent(3, test_obj, test_obj.fun, "parameter 1", "parameter 2")
        self.assertTrue(eq.hasNextEvent())

    def test_execute_next_event(self):
        eq = EventQueue()
        test_obj = TestObject()
        event1 = Event(1, test_obj, test_obj.fun, "parameter 1", "parameter 2")
        event2 = Event(2, test_obj, test_obj.fun, "parameter 3", "parameter 4")

        eq.queueEvent(event1)
        eq.queueEvent(event2)

        eq.executeNextEvent()
        eq.executeNextEvent()

        log = self.buffer.getvalue()

        expected_logs = "time is 1\nparameter 1 parameter 2\ntime is 2\nparameter 3 parameter 4\n"
        self.assertEqual(log, expected_logs)

if __name__ == "__main__":
    unittest.main()