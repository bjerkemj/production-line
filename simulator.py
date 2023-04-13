import datetime
import os
import sys
import io
from typing import List
import itertools
from batch import Batch 
from eventManager import EventQueue
from batch import batchGenerator
from productionLine import ProductionLine

class Simulator:

    def __init__(self, eventQueue: EventQueue, interval: int = 0, preLoadedBatches = []) -> None:
        self.eventQueue = eventQueue
        self.productionLine = ProductionLine(eventQueue)
        if preLoadedBatches:
            for batch, time in preLoadedBatches:
                self.eventQueue.createAndQueueEvent(time, self.productionLine.loadBatchToProductionLine, batch)
        else:
            starterBatchGenerator = batchGenerator(50)
            for i in range(20):
                starterBatch = next(starterBatchGenerator)
                self.eventQueue.createAndQueueEvent(i*interval, self.productionLine, self.productionLine.loadBatchToProductionLine, starterBatch)

    def setTaskPriority(self, unit1TaskList: List, unit2TaskList: List, unit3TaskList: List) -> None:
        self.productionLine.unit1TaskNumbers = unit1TaskList
        self.productionLine.unit2TaskNumbers = unit2TaskList
        self.productionLine.unit3TaskNumbers = unit3TaskList


    def run(self) -> None:
        counter = 0
        while self.eventQueue.hasNextEvent():
            self.eventQueue.executeNextEvent()
            counter += 1
        
        print('Number of events executed:', counter)
        self.finishTime = self.eventQueue.oldEvents[-1].time
        print('The simulation ended at time', self.finishTime)

    def printStatistics(self, comment: str = '')  -> None:
        print('Comment:', comment)
        seperator = ','
        numberWafersProduced = self.productionLine.buffers[-1].getNumberOfWafersInBuffer()
        totalTime = self.eventQueue.oldEvents[-1].time
        numBatches = len(self.productionLine.buffers[-1].batches)
        averageBatchSize = numberWafersProduced/numBatches
        print(str(numberWafersProduced), str(totalTime), str(numBatches), str(averageBatchSize), sep = seperator)



def main():
    unit1TaskNumbers = ['1', '3', '6', '9']
    unit2TaskNumbers = ['2', '5', '7']
    unit3TaskNumbers = ['4', '8']
    unit1PermuatiationList = list(itertools.permutations(unit1TaskNumbers))
    unit2PermuatiationList = list(itertools.permutations(unit2TaskNumbers))
    unit3PermuatiationList = list(itertools.permutations(unit3TaskNumbers))
    for prioUnit1 in unit1PermuatiationList:
        for prioUnit2 in unit2PermuatiationList:
            for prioUnit3 in unit3PermuatiationList:

                                  
                eventQueue = EventQueue()
                simulator = Simulator(eventQueue)
                old_stdout = sys.stdout
                sys.stdout = buffer = io.StringIO()
                simulator.run()
                pl = simulator.productionLine
                comment = f'U1: {prioUnit1}, U2: {prioUnit2}, U3: {prioUnit3}'
                simulator.printStatistics(comment)
                sys.stdout = old_stdout

                log = buffer.getvalue()

                ROOT = os.path.dirname(os.path.abspath(__file__))
                filename = datetime.datetime.now().strftime("%d-%m-%Y -%H-%M-%S")
                filepath = os.path.join(ROOT, 'simulations', filename)
                with open(filepath + '.txt', 'w') as file:
                    file.write(log)

if __name__ == '__main__':
    main()








