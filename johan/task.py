from typing import List
from buffer import Buffer
from batch import Batch

TASK_PROCESSING_TIME = {'1': .5, '2': 3.5, '3': 1.2, '4': 3, '5': .8, '6': .5, '7': 1, '8': 1.9, '9': .3}

class Task:
    def __init__(self, taskNumber: str, inputBuffer: Buffer, outputBuffer: Buffer = None) -> None:
        self.taskNumber = taskNumber
        self.inputBuffer = inputBuffer
        if outputBuffer:
            self.outputBuffer = outputBuffer
        else:
            self.outputBuffer = Buffer(str(int(taskNumber)+1))
        self.processingRate = TASK_PROCESSING_TIME[self.taskNumber]
        self.processingTime = 0
        self.loaded = False
        self.batch = None

    def __repr__(self) -> str:
        return f'Task {self.taskNumber}. Max input {self.getInputBuffer().capacity}. Max output {self.getOutputBuffer().capacity}'
    
    def setInputBuffer(self, inputBuffer: Buffer) -> None:
        self.inputBuffer = inputBuffer

    def getInputBuffer(self) -> Buffer:
        return self.inputBuffer
    
    def setOutputBuffer(self, outputBuffer: Buffer) -> None:
        self.outputBuffer = outputBuffer

    def getOutputBuffer(self) -> Buffer:
        return self.outputBuffer

    def hasBatchReadyToProcess(self) -> None:
        return self.inputBuffer.hasBatchReadyToProcess()
    
    def isLoaded(self) -> bool:
        return self.loaded
    
    def unload(self) -> None:
        self.getOutputBuffer().loadBatchToBuffer(self.batch)
        self.loaded = False
        self.batch = None

    def load(self) -> None:
        self.batch = self.getInputBuffer().unloadOldestBatchFromBuffer()
        self.loaded = True

    def hasPossibleAction(self) -> bool:
        return self.isLoaded() or len(self.getInputBuffer().batches)
    
    def getPossibleAction(self):
        if self.isLoaded():
            return self.unload
        return self.load

    def processNextBatch(self) -> None:
        if self.hasBatchReadyToProcess() and self.outputBuffer.canAddBatch(self.inputBuffer.getOldestBatchFromBuffer()):
            batchToProcess = self.inputBuffer.unloadOldestBatchFromBuffer()
            processingTime = batchToProcess.getBatchSize() * self.processingRate
            print(f'{str(batchToProcess)} processed in {str(self)} and took {processingTime} minutes')
            self.outputBuffer.loadBatchToBuffer(batchToProcess)
        else:
            print('No batches to process')
    
    def loadBatches(self, batches: List[Batch]) -> None:
        [self.inputBuffer.loadBatchToBuffer(batch) for batch in batches]

    
        