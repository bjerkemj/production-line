import datetime
import os
import sys
import io 
from eventManager import EventQueue
from batch import batchGenerator
from productionLine import ProductionLine
import logging
import time
# An event is on the form (time, object, function, paramtersOfFunction)



class Simulator:

    def __init__(self, eventQueue: EventQueue) -> None:
        self.eventQueue = eventQueue
        self.productionLine = ProductionLine(eventQueue)
        starterBatchGenerator = batchGenerator(50)
        for i in range(20):
            starterBatch = next(starterBatchGenerator)
            self.eventQueue.createAndQueueEvent(i*0, self.productionLine, self.productionLine.loadBatchToProductionLine, starterBatch)


    def run(self) -> None:
        counter = 0
        while self.eventQueue.hasNextEvent():
            self.eventQueue.executeNextEvent()
            counter += 1
        
        print('Number of events executed:', counter)
        self.finishTime = self.eventQueue.oldEvents[-1].time

    def printStatistics(self, comment: str = '')  -> None:
        print('Comment:', comment)
        seperator = ','
        numberWafersProduced = self.productionLine.buffers[-1].getNumberOfWafersInBuffer()
        totalTime = self.eventQueue.oldEvents[-1].time
        numBatches = len(self.productionLine.buffers[-1].batches)
        averageBatchSize = numberWafersProduced/numBatches
        print(str(numberWafersProduced), str(totalTime), str(numBatches), str(averageBatchSize), sep = seperator)







def main():
    eventQueue = EventQueue()
    simulator = Simulator(eventQueue)
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()
    simulator.run()
    pl = simulator.productionLine
    simulator.printStatistics()
    sys.stdout = old_stdout
    
    log = buffer.getvalue()

    ROOT = os.path.dirname(os.path.abspath(__file__))
    filename = datetime.datetime.now().strftime("%d-%m-%Y -%H-%M-%S")
    filepath = os.path.join(ROOT, 'simulations', filename)
    with open(filepath + '.txt', 'w') as file:
        file.write(log)






    

if __name__ == '__main__':
    main()








