from typing import List
from task import Task

class Unit:

    def __init__(self, unitNumber: str, tasks: List[Task]) -> None:
        self.unitNumber = unitNumber
        self.tasks = tasks

    def __repr__(self) -> str:
        return f'Unit {self.unitNumber}'
        

    def processNextBatch(self) -> None:
        if any([task.hasBatchReadyToProcess() for task in self.tasks]):
            for task in self.tasks:
                if task.hasBatchReadyToProcess():
                    task.processNextBatch()
                    break
        else:
            print(str(self), 'has no batches to process.')

