from typing import List
from task import Task

class Unit:

    def __init__(self, unitNumber: str, tasks: List[Task], taskPriority: List[int]) -> None:
        self.unitNumber = unitNumber
        self.tasks = tasks
        self.taskPriority = taskPriority

    def __repr__(self) -> str:
        return f'Unit {self.unitNumber}'
    
    def getTask(self, i: int):
        for task in self.tasks:
            if int(task.getTaskNumber()) == i:
                return task

    def processNextBatch(self) -> None:
        if any([task.hasBatchReadyToProcess() for task in self.tasks]):
            print(str(self), 'is processing a batch')
            for task in self.tasks:
                if task.hasBatchReadyToProcess():
                    task.processNextBatch()
                    break
        else:
            print(str(self), 'has no batches to process.')
        
    def getPossibleAction(self):
        for i in self.taskPriority:
            task = self.getTask(i)
            if task.hasPossibleAction():
                return task.getPossibleAction()
        return None