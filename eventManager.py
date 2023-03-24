class TestObject:

    def fun(self, time, param1, param2):
        print('time is', time)
        print(param1, param2)


class Event:

    def __init__(self, time: float, object: object, function, *args) -> None:
        self.time = time
        self.object = object
        self.function = function
        self.functionParameters = args

    def executeEvent(self) -> None:
        self.function(self.time, *self.functionParameters)

    def __repr__(self) -> str:
        return f'Event at time {self.time} on object {str(self.object)} is function {self.function.__name__} with args {self.functionParameters}'



class EventQueue:
    def __init__(self) -> None:
        self.time = 0
        self.eventset = []
        self.oldEvents = []

    def queueEvent(self, event: Event) -> None:
        if self.isEmpty():
            self.eventset.append(event)
        else:
            priorityIndex = self.getEventPriorityIndex(event)
            self.eventset.insert(priorityIndex, event)

    def getEventPriorityIndex(self, event: Event) -> int:
        for idx, eventTime in enumerate([event.time for event in self.eventset]):
            if event.time <= eventTime:
                return idx
        return len(self.eventset)

    def isEmpty(self) -> bool:
        return len(self.eventset) == 0

    def createAndQueueEvent(self, time:float, object:object, function, *args) -> None:
        event = Event(time, object, function, *args)
        self.queueEvent(event)

    def hasNextEvent(self) -> bool:
        return not self.isEmpty()
    
    def executeNextEvent(self) -> None:
        if self.hasNextEvent():
            if self.eventset[0].time < self.time:
                print('Some error must have occured since an event in queue is back in time')
            else:
                event = self.eventset.pop(0)
                self.oldEvents.append(event)
                self.time = event.time
                event.executeEvent()
        else:
            print('no more events')