from typing import List
from eventManager import EventQueue
from batch import Batch
from batch import batchGenerator

BUFFER_LOAD_TIME = 1 # minute

class Buffer:
    def __init__(self, bufferNumber: str, eventQueue = EventQueue, capacity: int = 120, isFinalBuffer : bool = False, isFirstBuffer:bool = False) -> None:
        self.bufferNumber = bufferNumber
        self.eventQueue = eventQueue
        self.capacity = capacity
        self.batches = []
        self.numberOfWafersInBuffer = 0
        self.isFinalBuffer = isFinalBuffer
        self.isFirstBuffer = isFirstBuffer
        self.nextTask = None
        self.productionLine = None

    def setProductionLine(self, productionLine) -> None:
        self.productionLine = productionLine

    def __repr__(self) -> str:
        return f'Buffer {self.bufferNumber}'
    
    def setNextTask(self, task) -> None:
        self.nextTask = task

    def getBatches(self) -> List[Batch]:
        return self.batches
    
    def getBufferNumber(self) -> str:
        return self.bufferNumber
    
    def getCapacity(self) -> int:
        return self.capacity
    
    def getNumberOfWafersInBuffer(self) -> int:
        return self.numberOfWafersInBuffer

    def loadBatchToBuffer(self, time: float, batch: Batch) -> None:
        """ Needs time management """
        if self.canAddBatch(batch):
            self.batches.append(batch)
            print(f'{str(batch)} loaded to {str(self)}')
            self.updateNumberOfWafersInBuffer()
            if self.isFinalBuffer:
                print(f'Finished processing batch {str(batch)}. It is now in the final buffer at time {time}. Total number of wafers produced: {self.numberOfWafersInBuffer}')
            else:
                self.nextTask.notifyBufferIsInQueue(time)
                print(f'{str(self)} now contains {self.numberOfWafersInBuffer} wafers')
                if self.isFirstBuffer and self.numberOfWafersInBuffer < 70: # Makes sure there are always 70+ wafers in the first buffer
                    starterBatch = next(batchGenerator())
                    self.eventQueue.createAndQueueEvent(time, self.productionLine, self.productionLine.loadBatchToProductionLine, starterBatch)

        else:
            print('ERROR. Some1 tried to load to a buffer that was full...')

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
    

        
        
    

