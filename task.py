# Tinus F Alsos and Johan Bjerkem
from buffer import Buffer
from eventManager import EventQueue

TASK_PROCESSING_TIME = {'1': .5, '2': 3.5, '3': 1.2, '4': 3, '5': .8, '6': .5, '7': 1, '8': 1.9, '9': .3}

class Task:
    UNLOADTIME = 1

    def __init__(self, taskNumber: str, inputBuffer: Buffer, outputBuffer: Buffer, eventQueue: EventQueue) -> None:
        self.taskNumber = taskNumber
        self.inputBuffer = inputBuffer
        self.inputBuffer.setNextTask(self)
        self.outputBuffer = outputBuffer
        self.outputBuffer.setPrevTask(self)
        self.processingRate = TASK_PROCESSING_TIME[self.taskNumber]
        self.eventQueue = eventQueue
        self.unit = None

    def __repr__(self) -> str:
        return f'Task {self.taskNumber}'
    
    def getTaskNumber(self) -> str:
        return self.taskNumber
    
    def setUnit(self, unit) -> None:
        self.unit = unit
    
    def setInputBuffer(self, inputBuffer: Buffer) -> None:
        self.inputBuffer = inputBuffer

    def getInputBuffer(self) -> Buffer:
        return self.inputBuffer
    
    def setOutputBuffer(self, outputBuffer: Buffer) -> None:
        self.outputBuffer = outputBuffer

    def getOutputBuffer(self) -> Buffer:
        return self.outputBuffer

    def hasBatchReadyToProcess(self) -> None:
        if self.inputBuffer.hasBatchReadyToProcess():
            oldestBatch = self.inputBuffer.getOldestBatchFromBuffer()
            return self.outputBuffer.canAddBatch(oldestBatch)
        return False
    
    def notifyBufferIsInQueue(self, time: float) -> None:
        self.unit.notifyTaskIsInQueue(time)

    def processNextBatch(self, time) -> None:
        # Mangler time management
        if self.hasBatchReadyToProcess():
            print(f"{str(self)} begins processing batch {str(self.inputBuffer.getOldestBatchFromBuffer())} at time {time}")
            batchToProcess = self.inputBuffer.unloadOldestBatchFromBuffer(time)
            if self.inputBuffer.getPrevTask():
                taskToNotify = self.inputBuffer.getPrevTask()
                taskToNotify.notifyBufferIsInQueue(time)
            self.outputBuffer.reserveSpace(batchToProcess.getBatchSize())
            processingTime = batchToProcess.getBatchSize() * self.processingRate
            newTime = time + processingTime + Task.UNLOADTIME*2
            print(f'{str(batchToProcess)} processed in {str(self)} and took {processingTime} minutes finishing at {newTime}')
            self.eventQueue.createAndQueueEvent(newTime, self.outputBuffer, self.outputBuffer.loadBatchToBuffer, batchToProcess)
            self.eventQueue.createAndQueueEvent(newTime, self.unit, self.unit.setIdleToTrue)
            
        else:
            print('No batches to process')

        