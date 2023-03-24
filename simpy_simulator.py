import simpy
from batch import Batch
import task

# Inspo:
# https://www.youtube.com/watch?v=QV-pJnKrGuc

class GlobalVariables:
    TASK_PROCESSING_TIME = task.TASK_PROCESSING_TIME
    batch_size = 20
    maxNumberOfWafers = 40
    loadTime = 1


class ProductionLineModel:

    def __init__(self):
        self.env = simpy.Environment()
        self.wafersFinished = 0
        self.wafersInSystem = 0
        self.batchNumber = 0
        
        self.unit1 = simpy.Resource(self.env, capacity=1)
        self.unit2 = simpy.Resource(self.env, capacity=1)
        self.unit3 = simpy.Resource(self.env, capacity=1)

        self.units = [self.unit1, self.unit2, self.unit3]

        # Capacity of 6 since we model with fixed batch size of 20
        self.buffer0 = simpy.Store(self.env, capacity = 6) 
        self.buffer1 = simpy.Store(self.env, capacity = 6)
        self.buffer2 = simpy.Store(self.env, capacity = 6)
        self.buffer3 = simpy.Store(self.env, capacity = 6)
        self.buffer4 = simpy.Store(self.env, capacity = 6)
        self.buffer5 = simpy.Store(self.env, capacity = 6)
        self.buffer6 = simpy.Store(self.env, capacity = 6)
        self.buffer7 = simpy.Store(self.env, capacity = 6)
        self.buffer8 = simpy.Store(self.env, capacity = 6)
        self.buffer9 = simpy.Store(self.env, capacity = 6)

        self.buffers = [self.buffer0, self.buffer1, self.buffer2, self.buffer3, self.buffer4, self.buffer5, self.buffer6, self.buffer7, self.buffer8, self.buffer9]

    def addNewBatchToProductionLine(self):
        # Må fikse opp i bruken av Store. under her (ikke self.buffer0.request...)
        
        while self.wafersInSystem < GlobalVariables.maxNumberOfWafers:
            # Iterate unique batch number
            self.batchNumber += 1
            # Create a new batch
            batch = Batch(str(self.batchNumber), GlobalVariables.batch_size)
            timeBatchCreated = self.env.now
            self.wafersInSystem += batch.getBatchSize()
            print(f'Batch {self.batchNumber} was created at {timeBatchCreated}')
            with self.buffer0.request() as req:
                yield req
                timeBatchAddedToBuffer0 = self.env.now
                print(f'Batch {batch.batchNumber} waited {timeBatchAddedToBuffer0 - timeBatchCreated} minutes before being loaded to buffer0')
                
                self.env.process(self.addBatchToUnit1Queue(batch))

                yield self.env.timeout(GlobalVariables.loadTime)



        
    def addBatchToUnit1Queue(self, batch: Batch):

        print(f'{str(batch)} was added to unit1 queue at {self.env.now}')

        with self.unit1.request() as req:
            yield req

            with self.buffer1 as req: # Because we also need to wait for buffer1 to be free
                yield req

            print(f'{str(batch)} is processed in Task 1 at {self.env.now}')

            timeToProcessBatch = GlobalVariables.TASK_PROCESSING_TIME['1'] * batch.getBatchSize()

            yield self.env.timeout(timeToProcessBatch)
        
        with self.buffer1 as req:
            yield req

            self.env.timeout(GlobalVariables.loadTime)












        
        





def main():

    # Set up event simulation:
    env = simpy.Environment()

    # Set up resources (trenger batch capacity være med her?):
    unit1 = simpy.Resource(env, capacity=1)
    unit2 = simpy.Resource(env, capacity=1)
    unit3 = simpy.Resource(env, capacity=1)

    # Paramter values if needed here:


    # Start arrivals generator (in our case we create a deterministic generator maybe?):

    # Run the simulation:
    env.run() # Stops when there are no events to process


if __name__ == '__main__':
    main()


