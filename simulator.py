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

    def __init__(self, eventQueue: EventQueue, batchSize: int = 50, interval: int = 0, preLoadedBatches = []) -> None:
        self.eventQueue = eventQueue
        self.productionLine = ProductionLine(eventQueue)
        if preLoadedBatches:
            for batch, time in preLoadedBatches:
                self.eventQueue.createAndQueueEvent(time, self.productionLine.loadBatchToProductionLine, batch)
        else:
            starterBatchGenerator = batchGenerator(batchSize)
            numFullBatches = 1000//batchSize
            remainder = 1000 - numFullBatches*batchSize
            if remainder == 0:
                for i in range(numFullBatches):
                    starterBatch = next(starterBatchGenerator)
                    self.eventQueue.createAndQueueEvent(i*interval, self.productionLine, self.productionLine.loadBatchToProductionLine, starterBatch)
            else:
                for i in range(numFullBatches - 1):
                    starterBatch = next(starterBatchGenerator)
                    self.eventQueue.createAndQueueEvent(i*interval, self.productionLine, self.productionLine.loadBatchToProductionLine, starterBatch)
                finalBatch = Batch(str(numFullBatches), remainder + batchSize)
                self.eventQueue.createAndQueueEvent((numFullBatches-1)*interval, self.productionLine, self.productionLine.loadBatchToProductionLine, finalBatch)
                

    def setTaskPriority(self, unit1TaskList: List, unit2TaskList: List, unit3TaskList: List) -> None:
        self.productionLine.units[0].setTaskPriority(unit1TaskList)
        self.productionLine.units[1].setTaskPriority(unit2TaskList)
        self.productionLine.units[2].setTaskPriority(unit3TaskList)



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
        print(str(numberWafersProduced), str(round(totalTime, 1)), str(numBatches), str(averageBatchSize), sep = seperator)



def main():

    batchSizes = list(range(20, 51))
    for batchSize in batchSizes:
        eventQueue = EventQueue()
        simulator = Simulator(eventQueue, batchSize = batchSize)
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        simulator.run()
        pl = simulator.productionLine
        comment = f'Batch size: {batchSize}'
        simulator.printStatistics(comment)
        sys.stdout = old_stdout
        log = buffer.getvalue()

        ROOT = os.path.dirname(os.path.abspath(__file__))
        filename = datetime.datetime.now().strftime("%d-%m-%Y -%H-%M-%S")
        filepath = os.path.join(ROOT, 'simulations_batchSize2', filename + str(batchSize))
        with open(filepath + '.txt', 'w') as file:
            file.write(log)

def main2():
    unit1TaskNumbers = ['1', '3', '6', '9']
    unit2TaskNumbers = ['2', '5', '7']
    unit3TaskNumbers = ['4', '8']
    unit1PermuatiationList = list(itertools.permutations(unit1TaskNumbers))
    unit2PermuatiationList = list(itertools.permutations(unit2TaskNumbers))
    unit3PermuatiationList = list(itertools.permutations(unit3TaskNumbers))
    counter = 0
    for prioUnit1 in unit1PermuatiationList:
        for prioUnit2 in unit2PermuatiationList:
            for prioUnit3 in unit3PermuatiationList:
                counter += 1
                eventQueue = EventQueue()
                simulator = Simulator(eventQueue)
                simulator.setTaskPriority(prioUnit1, prioUnit2, prioUnit3)
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
                filepath = os.path.join(ROOT, 'simulations_orderingHeuristic_del', filename + str(counter))
                with open(filepath + '.txt', 'w') as file:
                    file.write(log)

if __name__ == '__main__':
    main()








