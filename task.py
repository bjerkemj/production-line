
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
        if self.hasBatchReadyToProcess():
            batchToProcess = self.inputBuffer.unloadOldestBatchFromBuffer()
            processingTime = batchToProcess.getBatchSize() * self.processingRate
            if self.outputBuffer.canAddBatch(batchToProcess):
                self.outputBuffer.loadBatchToBuffer(batchToProcess)
            else:
                print(f'{str(batchToProcess)} was processed in task {self.taskNumber} but the outbutBuffer {self.outputBuffer.getBufferNumber()} did not have the capacity to load the batch so the batch was discarded')
        else:
            print('No batches to process')

    
        