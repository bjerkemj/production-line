# Tinus F Alsos and Johan Bjerkem
from typing import List
from task import Task
from eventManager import EventQueue

class Unit:
    def __init__(self, unitNumber: str, eventQueue: EventQueue = EventQueue, tasks: List[Task] = []) -> None:
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

    def setTaskPriority(self, priorityTaskList: List[int]) -> None:
        newTaskList = []
        for taskID in priorityTaskList:
            for task in self.tasks:
                if task.getTaskNumber()== taskID:
                    newTaskList.append(task)
                    break
        self.tasks = newTaskList

    def notifyTaskIsInQueue(self, time: float) -> None:
         if self.idle:
             self.eventQueue.createAndQueueEvent(time, self, self.processNextBatch)

    def setIdleToTrue(self, time: float) -> None:
        print(f'{str(self)} is set idle to true at {time}')
        self.idle = True
        self.eventQueue.createAndQueueEvent(time, self, self.processNextBatch)

    def processNextBatch(self, time: float) -> None:
        if self.idle:
            if any([task.hasBatchReadyToProcess() for task in self.tasks]):
                print(str(self), 'is processing a batch at time', time)
                for task in self.tasks:
                    if task.hasBatchReadyToProcess():
                        self.idle = False
                        task.processNextBatch(time)
                        return
                raise Exception
            else:
                print(str(self), 'has no batches to process at time', time)
        else:
            print(str(self) + ' is not idle. Cannot process at current time.')

