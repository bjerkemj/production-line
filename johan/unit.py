from typing import List
from task import Task

class Unit:

    def __init__(self, unitNumber: str, tasks: List[Task], unitPriority: List[int]) -> None:
        self.unitNumber = unitNumber
        self.tasks = tasks
        self.unitPriority = unitPriority

    def __repr__(self) -> str:
        return f'Unit {self.unitNumber}'


    def processNextBatch(self) -> None:
        if any([task.hasBatchReadyToProcess() for task in self.tasks]):
            print(str(self), 'is processing a batch')
            for task in self.tasks:
                if task.hasBatchReadyToProcess():
                    task.processNextBatch()
                    break
        else:
            print(str(self), 'has no batches to process.')
        
    def getPossibleAction(self) -> List:
        actions = []
        for task in self.tasks:
            if task.hasPossibleAction():
                actions.append(task.getPossibleAction())
        return actions