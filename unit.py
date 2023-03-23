from typing import List
from task import Task
from eventManager import EventQueue

class Unit:

    def __init__(self, unitNumber: str, eventQueue = EventQueue, tasks: List[Task] = []) -> None:
        self.unitNumber = unitNumber
        self.eventQueue = eventQueue
        self.tasks = tasks
        self.idle = True
        for task in tasks:
            task.setUnit(self)

    def __repr__(self) -> str:
        return f'Unit {self.unitNumber}'
    
    def addTask(self, task: Task) -> None:
        self.tasks.append(task)

    def notifyTaskIsInQueue(self, time) -> None:
         if self.idle:
             self.idle = False
             self.eventQueue.createAndQueueEvent(time, self, self.processNextBatch)

    def setIdleToTrue(self, time) -> None:
        self.idle = True
        self.eventQueue.createAndQueueEvent(time, self, self.processNextBatch)


    def processNextBatch(self, time) -> None:
        if any([task.hasBatchReadyToProcess() for task in self.tasks]):
            print(str(self), 'is processing a batch at time', time)
            for task in self.tasks:
                if task.hasBatchReadyToProcess():
                    task.processNextBatch(time)
                    return
        else:
            print(str(self), 'has no batches to process at time', time)

