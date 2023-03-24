from productionLine import ProductionLine
from batch import Batch

if __name__ == '__main__':

    pl = ProductionLine()
    print('Production Line initiated')
    batch = Batch('1', 20)
    pl.loadBatchToProductionLine(batch)
    unit1, unit2, unit3 = [unit for unit in pl.units]

    unit1.processNextBatch()
    unit2.processNextBatch()
    unit1.processNextBatch()
    unit3.processNextBatch()
    unit2.processNextBatch()
    unit1.processNextBatch()
    unit2.processNextBatch()
    unit3.processNextBatch()
    unit1.processNextBatch()
