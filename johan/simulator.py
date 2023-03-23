
from johan import ProductionLine
from batch import Batch

class Simulator:
    def __init__(self, maxWafers: int = 1000) -> None:
        self.p = ProductionLine(maxWafers)

    def simulateOneBatch(self):
        time = 0
        batch = Batch("1", 20)
        batches = [batch]
        
        actions = []
        standByUnits = [self.p.getUnits()]
        busyUnits = []
        
        while True:
            if len(batches):
                actions.append(self.p.loadBatches)
            for unit in standByUnits:
                unit.


    
    
if __name__ == "__main__":
    s = Simulator()
    print(s.p.getTasks())

    unit1priority = [1,3,6,9]
    unit2priority = [2,5,7]
    unit1priority = [4,8]

