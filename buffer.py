from typing import List
from batch import Batch


class Buffer:
    def __init__(self, bufferNumber: str, capacity: int = 120) -> None:
        self.bufferNumber = bufferNumber
        self.capacity = capacity
        self.batches = []
        self.numberOfWafersInBuffer = 0

    def getBatches(self) -> List[Batch]:
        return self.batches

    def addBatch(self, batch: Batch) -> None:
        if self.canAddBatch(batch):
            self.batches.append(batch)
            self.updateNumberOfWafersInBuffer()

    def canAddBatch(self, batch: Batch) -> bool:
        return batch.batchSize + self.numberOfWafersInBuffer <= self.capacity

    def updateNumberOfWafersInBuffer(self) -> None:
        self.numberOfWafersInBuffer = sum(
            [batch.getBatchSize() for batch in self.batches]
        )

    