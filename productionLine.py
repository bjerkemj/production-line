import math
from batch import Batch
from buffer import Buffer
from task import Task
from unit import Unit


class ProductionLine:

    unit1TaskNumbers = ['1', '3', '6', '9']
    unit2TaskNumbers = ['2', '5', '7']
    unit3TaskNumbers = ['4', '8']

    def __init__(self) -> None:
        self.buffers = []
        self.tasks = []
        self.buffers.append(Buffer('0'))
        for i in range(1, 10):
            idNumber = str(i)
            self.buffers.append(Buffer(idNumber))
            self.tasks.append(Task(idNumber, self.buffers[-2], self.buffers[-1]))
        self.buffers[-1].capacity = math.inf
        self.buffers[-1].isFinalBuffer = True
        unit1 = Unit('1', [task for task in self.tasks if task.taskNumber in ProductionLine.unit1TaskNumbers])
        unit2 = Unit('2', [task for task in self.tasks if task.taskNumber in ProductionLine.unit2TaskNumbers])
        unit3 = Unit('3', [task for task in self.tasks if task.taskNumber in ProductionLine.unit3TaskNumbers])
        self.units = [unit1, unit2, unit3]

    

    def loadBatchToProductionLine(self, batch: Batch) -> None:
        if self.buffers[0].canAddBatch(batch):
            self.buffers[0].loadBatchToBuffer(batch)

    
if __name__ == '__main__':
    pl = ProductionLine()
    batch = Batch('1', 20)
    print(batch.batchNumber)
    print(batch.batchSize)
    pl.loadBatchToProductionLine(batch)

    newline = "\n"
    for unit in pl.units:
        print(f'{str(unit)}, has tasks:')
        print(newline.join(f'{str(task)} with inputBuffer {str(task.inputBuffer)} and outputBuffer {str(task.outputBuffer)}' for task in unit.tasks))

    print(pl.units[0].tasks[-1].outputBuffer.isFinalBuffer)





    
