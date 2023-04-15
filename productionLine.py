# Tinus F Alsos and Johan Bjerkem
import math
from batch import Batch
from buffer import Buffer
from task import Task
from unit import Unit
from eventManager import EventQueue

class ProductionLine:
    unit1TaskNumbers = ['1', '3', '9', '6']
    unit2TaskNumbers = ['5', '7', '2']
    unit3TaskNumbers = ['4', '8']

    def __init__(self, eventQueue: EventQueue = EventQueue()) -> None:
        self.buffers = []
        self.tasks = []
        self.buffers.append(Buffer('0', eventQueue, isFirstBuffer=True, capacity=math.inf))
        for i in range(1, 10):
            idNumber = str(i)
            self.buffers.append(Buffer(idNumber, eventQueue))
            self.tasks.append(Task(idNumber, self.buffers[-2], self.buffers[-1], eventQueue))
        self.buffers[-1].capacity = math.inf
        self.buffers[-1].isFinalBuffer = True
        self.buffers[0].setProductionLine(self)
        unit1 = Unit('1', eventQueue, [task for task in self.tasks if task.taskNumber in ProductionLine.unit1TaskNumbers])
        unit2 = Unit('2', eventQueue, [task for task in self.tasks if task.taskNumber in ProductionLine.unit2TaskNumbers])
        unit3 = Unit('3', eventQueue, [task for task in self.tasks if task.taskNumber in ProductionLine.unit3TaskNumbers])
        unit1.setTaskPriority(ProductionLine.unit1TaskNumbers)
        unit2.setTaskPriority(ProductionLine.unit2TaskNumbers)
        unit3.setTaskPriority(ProductionLine.unit3TaskNumbers)

        self.units = [unit1, unit2, unit3]
        self.eventQueue = eventQueue

    def loadBatchToProductionLine(self, time:float, batch: Batch) -> None:
        if self.buffers[0].canAddBatch(batch):
            self.buffers[0].reserveSpace(batch.getBatchSize())
            self.buffers[0].loadBatchToBuffer(time, batch)
        else:
            print("Couldn't load batch, trying again at time", time + 50)
            self.eventQueue.createAndQueueEvent(time + 1, self, self.loadBatchToProductionLine, batch)

if __name__ == '__main__':
    pl = ProductionLine()
    batch = Batch('1', 20)
    print(batch.getBatchNumber())
    print(batch.getBatchSize())
    pl.loadBatchToProductionLine(0,batch)

    newline = "\n"
    for unit in pl.units:
        print(f'{str(unit)}, has tasks:')
        print(newline.join(f'{str(task)} with inputBuffer {str(task.inputBuffer)} and outputBuffer {str(task.outputBuffer)}' for task in unit.tasks))

    print(pl.units[0].tasks[-1].outputBuffer.isFinalBuffer)
