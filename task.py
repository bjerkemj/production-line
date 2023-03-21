
from buffer import Buffer

TASK_PROCESSING_TIME = {'1': .5, '2': 3.5, '3': 1.2, '4': 3, '5': .8, '6': .5, '7': 1, '8': 1.9, '9': .3}


class Task:

    def __init__(self, taskNumber: str, inputBuffer: Buffer, outputBuffer: Buffer) -> None:
        self.taskNumber = taskNumber
        self.inputBuffer = inputBuffer
        self.outputBuffer = outputBuffer
        self.processingRate = TASK_PROCESSING_TIME[self.taskNumber]

    def __repr__(self) -> str:
        return f'Task {self.taskNumber}'

    def hasBatchReadyToProcess(self) -> None:
        return self.inputBuffer.hasBatchReadyToProcess()

    def processNextBatch(self) -> None:
        # Mangler time management
        if self.hasBatchReadyToProcess() and self.outputBuffer.canAddBatch(self.inputBuffer.getOldestBatchFromBuffer()):
            batchToProcess = self.inputBuffer.unloadOldestBatchFromBuffer()
            processingTime = batchToProcess.getBatchSize() * self.processingRate
            print(f'{str(batchToProcess)} processed in {str(self)} and took {processingTime} minutes')
            self.outputBuffer.loadBatchToBuffer(batchToProcess)
        else:
            print('No batches to process')

    
        