

class Batch:

    def __init__(self, batchNumber: str, batchSize: int) -> None:
        self.batchNumber = batchNumber
        self.batchSize = batchSize

    def __repr__(self) -> str:
        return f'Batch {self.batchNumber} of size {self.batchSize}'
    
    def getBatchSize(self) -> int:
        return self.batchNumber
    
    def getBatchNumbers(self) -> str:
        return self.batchNumber