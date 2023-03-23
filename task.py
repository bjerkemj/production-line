
from buffer import Buffer
from eventManager import EventQueue

TASK_PROCESSING_TIME = {'1': .5, '2': 3.5, '3': 1.2, '4': 3, '5': .8, '6': .5, '7': 1, '8': 1.9, '9': .3}


class Task:
    UNLOADTIME = 1

    def __init__(self, taskNumber: str, inputBuffer: Buffer, outputBuffer: Buffer, eventQueue: EventQueue, isAvailable = True) -> None:
        self.taskNumber = taskNumber
        self.inputBuffer = inputBuffer
        self.inputBuffer.setNextTask(self)
        self.outputBuffer = outputBuffer
        self.processingRate = TASK_PROCESSING_TIME[self.taskNumber]
        self.eventQueue = eventQueue
        self.unit = None

    def setUnit(self, unit) -> None:
        self.unit = unit

    def __repr__(self) -> str:
        return f'Task {self.taskNumber}'
    
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
    
    def notifyBufferIsInQueue(self, time: float) -> None:
        self.unit.notifyTaskIsInQueue(time)

    def processNextBatch(self, time) -> None:
        # Mangler time management
        if self.hasBatchReadyToProcess() and self.outputBuffer.canAddBatch(self.inputBuffer.getOldestBatchFromBuffer()):
            batchToProcess = self.inputBuffer.unloadOldestBatchFromBuffer()
            processingTime = batchToProcess.getBatchSize() * self.processingRate
            print(f'{str(batchToProcess)} processed in {str(self)} and took {processingTime} minutes')
            newTime = time + processingTime + Task.UNLOADTIME
            self.eventQueue.createAndQueueEvent(newTime, self.outputBuffer, self.outputBuffer.loadBatchToBuffer, batchToProcess)

            self.eventQueue.createAndQueueEvent(newTime, self.unit, self.unit.setIdleToTrue)
        else:
            print('No batches to process')

    
        