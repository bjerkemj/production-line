from batch import Batch
from buffer import Buffer
from task import Task
from unit import Unit
from typing import List


class ProductionLine:

    unit1TaskNumbers = ['1', '3', '6', '9']
    unit2TaskNumbers = ['2', '5', '7']
    unit3TaskNumbers = ['4', '8']

    def __init__(self, maxWafers: int = 1000, unit1priority: List[int] = [1,3,6,9], unit2priority: List[int] = [2,5,7], unit3priority: List[int] = [4,8]) -> None:
        self.maxWafers = 1000
        self.tasks = []
        self.tasks.append(Task('1', Buffer('1', self.maxWafers)))

        for i in range(2, 9):
            idNumber = str(i)
            inputBuffer = self.tasks[i-2].getOutputBuffer()
            self.tasks.append(Task(idNumber, inputBuffer))
        inputBuffer = self.tasks[7].getOutputBuffer()
        self.tasks.append(Task('9', inputBuffer, Buffer('11', self.maxWafers)))


        unit1 = Unit('1', [task for task in self.tasks if task.taskNumber in ProductionLine.unit1TaskNumbers], unit1priority)
        unit2 = Unit('2', [task for task in self.tasks if task.taskNumber in ProductionLine.unit2TaskNumbers], unit2priority)
        unit3 = Unit('3', [task for task in self.tasks if task.taskNumber in ProductionLine.unit3TaskNumbers], unit3priority)
        self.units = [unit1, unit2, unit3]

        self.time = 0

    def getTasks(self) -> List[Task]:
        return self.tasks

    def getInputBuffer(self) -> Buffer:
        return self.getTasks()[0].getInputBuffer()
    
    def getOutputBuffer(self) -> Buffer:
        return self.getTasks()[-1].getOutputBuffer()

    def loadBatches(self, batches: List[Batch]) -> None:
        self.tasks[0].loadBatches(batches)

    def getPossibleActions(self) -> List:
        actions = []
        for unit in self.units:
            unitActions = unit.getPossibleAction()
            if unitActions:
                for action in unitActions:
                    actions.append(action)
        return actions

    def getUnits(self):
        return self.units
    
    def simulate(self) -> None:
        time = 1 # for loading the shit
        totalWafers = self.getInputBuffer().getNumberOfWafersInBuffer()
        while totalWafers != self.getOutputBuffer().getNumberOfWafersInBuffer():
            possibleActions = self.getPossibleActions()
            possibleActions[0]()    
            



if __name__ == '__main__':
    pl = ProductionLine()
    batch1 = Batch('1', 20)
    batch2 = Batch('2', 20)
    batch3 = Batch('3', 20)
    batches = [batch1]
  
    # [print(task) for task in pl.getTasks()]
    
    pl.loadBatches(batches)

    print("\nStart: ")
    pl.simulate()


    # print(batch.batchNumber)
    # print(batch.batchSize)
    # pl.loadBatchToProductionLine(batch)

    # newline = "\n"
    # for unit in pl.units:
    #     print(f'{str(unit)}, has tasks:')
    #     print(newline.join(f'{str(task)} with inputBuffer {str(task.inputBuffer)} and outputBuffer {str(task.outputBuffer)}' for task in unit.tasks))

    # print(pl.units[0].tasks[-1].outputBuffer.isFinalBuffer)





    
