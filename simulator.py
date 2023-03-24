from eventManager import EventQueue
from batch import batchGenerator
from productionLine import ProductionLine
# An event is on the form (time, object, function, paramtersOfFunction)



class Simulator:

    def __init__(self, eventQueue: EventQueue) -> None:
        self.eventQueue = eventQueue
        self.productionLine = ProductionLine(eventQueue)
        time = 0.0
        starterBatchGenerator = batchGenerator()
        for i in range(50):
            starterBatch = next(starterBatchGenerator)
            self.eventQueue.createAndQueueEvent(time + 20*i, self.productionLine, self.productionLine.loadBatchToProductionLine, starterBatch)


    def run(self) -> None:
        counter = 0
        while self.eventQueue.hasNextEvent():
            self.eventQueue.executeNextEvent()
            counter += 1
        
        print('Number of events executed:', counter)





def main():
    eventQueue = EventQueue()
    simulator = Simulator(eventQueue)
    simulator.run()
    pl = simulator.productionLine
    # print(pl.buffers[9].getNumberOfWafersInBuffer())
    # print(str(pl.buffers[2]))
    # print(pl.buffers[2].nextTask.unit.idle)
    # print(simulator.productionLine.buffers[2].getNumberOfWafersInBuffer())
    # print([str(task) for task in simulator.productionLine.buffers[2].nextTask.unit.tasks])
    print([buffer.getNumberOfWafersInBuffer() for buffer in pl.buffers])
    print([(str(task), task.processingRate) for task in pl.tasks])
    # print(pl.buffers[0].reservedSpace)
    # print(pl.buffers[0].reservedSpace)

    # print(len(pl.eventQueue.oldEvents))
    # for event in pl.eventQueue.oldEvents:
        # print(str(event))
    # print(pl.eventQueue.oldEvents)





    

if __name__ == '__main__':
    main()








