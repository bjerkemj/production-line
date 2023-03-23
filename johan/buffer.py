from typing import List
from batch import Batch

BUFFER_LOAD_TIME = 1

class Buffer:
    def __init__(self, bufferNumber: str, capacity: int = 120) -> None:
        self.bufferNumber = bufferNumber
        self.capacity = capacity
        self.batches = []
        self.numberOfWafersInBuffer = 0

    def __repr__(self) -> str:
        return f'Buffer {self.bufferNumber}'

    def getBatches(self) -> List[Batch]:
        return self.batches
    
    def getBufferNumber(self) -> str:
        return self.bufferNumber
    
    def getCapacity(self) -> int:
        return self.capacity
    
    def getNumberOfWafersInBuffer(self) -> int:
        return self.numberOfWafersInBuffer

    def loadBatchToBuffer(self, batch: Batch) -> None:
        """ Needs time management """
        if self.canAddBatch(batch):
            self.batches.append(batch)
            print(f'{str(batch)} loaded to {str(self)}')
            self.updateNumberOfWafersInBuffer()
            print(f'{str(self)} now contains {self.numberOfWafersInBuffer} wafers')
        else:
            print("Batch was discarded")

    def canAddBatch(self, batch: Batch) -> bool:
        return batch.batchSize + self.numberOfWafersInBuffer <= self.capacity

    def updateNumberOfWafersInBuffer(self) -> None:
        self.numberOfWafersInBuffer = sum(
            [batch.getBatchSize() for batch in self.batches]
        )

    def unloadOldestBatchFromBuffer(self) -> Batch:
        """ Needs time management. Returns the batch first added to the buffer (FIFO). Should be changed later. """
        if self.hasBatchReadyToProcess():
            self.numberOfWafersInBuffer = self.numberOfWafersInBuffer - self.batches[0].getBatchSize()
            print(f'{str(self.batches[0])} unloaded from {str(self)}')
            print(f'{str(self)} now contains {self.numberOfWafersInBuffer} wafers')
            return self.batches.pop(0)
        
    def getOldestBatchFromBuffer(self) -> Batch:
        return self.batches[0]
        
    def hasBatchReadyToProcess(self) -> bool:
        return len(self.batches) > 0
    

        
        
    

