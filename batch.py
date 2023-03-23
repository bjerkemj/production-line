


class Batch:

    def __init__(self, batchNumber: str, batchSize: int) -> None:
        self.batchNumber = batchNumber
        self.batchSize = batchSize
        self.prevTask = 0
        self.prevBuffer = 0
        self.location = "Start"

    def __repr__(self) -> str:
        return f'Batch {self.batchNumber} of size {self.batchSize}'
    
    def getBatchSize(self) -> int:
        return self.batchSize
    
    def getBatchNumber(self) -> str:
        return self.batchNumber
    
    def getLocation(self):
        # Maybe location should be a buffer or a task/unit? Not sure
        return self.location
    
    def setLocation(self, location) -> str:
        self.location = location



def batchGenerator(batchSize: int = 20) -> Batch:
    batchNumber = 0
    while True:
        batchNumber += 1
        yield Batch(batchNumber, batchSize)