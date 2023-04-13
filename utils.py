import os
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.abspath(__file__))
folderName = 'simulations_plots'
SAVE_FOLDER = os.path.join(ROOT, 'simulations_plots')

def savePlotsFromSimulationsInFolder(folderName: str):
    folderPath = os.path.join(ROOT, folderName)
    for filepath in os.scandir(folderPath):
        fileName = os.path.basename(filepath.path)
        comment, finalStatsDict, finishedBatchTimes, numWafersProduced = getCommentAndDictionaryFromSimulation(filepath)
        fig, ax = plt.subplots()
        ax.plot(finishedBatchTimes, numWafersProduced)
        ax.grid()
        fig.suptitle(comment)
        ax.set_xlabel('Time [minutes]')
        ax.set_ylabel('Number of wafers produced')
        fig.savefig(os.path.join(SAVE_FOLDER, fileName[:-3] + 'png'))

def createSinglePlotFromFilesInFolder(folderName: str, save: bool = True):
    folderPath = os.path.join(ROOT, folderName)
    for filepath in os.scandir(folderPath):
        fileName = os.path.basename(filepath.path)
        comment, finalStatsDict, finishedBatchTimes, numWafersProduced = getCommentAndDictionaryFromSimulation(filepath)
        plt.plot(finishedBatchTimes, numWafersProduced, label = finalStatsDict)
    plt.legend()
    plt.xlabel('Time [minutes]')
    plt.ylabel('Number of wafers produced')
    if save:
        plt.savefig(os.path.join(SAVE_FOLDER, 'allPlots.png'))
    else:
        plt.show()



def getCommentAndDictionaryFromSimulation(filepath: str):
    with open(filepath, 'r') as file:
        lines = file.readlines()
        lines = [line.replace('\n', '') for line in lines]
        comment = lines[-2]
        finalStatsList = lines[-1].split(',')
        finalStatsDict = {'numWafers': int(finalStatsList[0]), 'prodTime': float(finalStatsList[1]), 'numBatches': int(finalStatsList[2]), 'avgBatchSize': finalStatsList[-1]}
        finishedBatchTimes = [0]
        numWafersProduced = [0]
        for line in lines:
            if 'Finished processing' in line:
                timeIndex = line.find('time') + 5 # length of 'time' pluss one space
                numDots = 0
                for i in range(timeIndex, len(line)):
                    if line[i] == '.':
                        numDots += 1
                        if numDots == 2:
                            endTimeIndex = i
                            break
                time = float(line[timeIndex:endTimeIndex])
                
                # Find the index of the number of wafers produced number
                counter = 0
                for char in reversed(line):
                    if char == ' ':
                        break
                    counter += 1
                    
                numWafers = int(line[len(line) - counter:])
                finishedBatchTimes.append(time)
                numWafersProduced.append(numWafers)
        return comment, finalStatsDict, finishedBatchTimes, numWafersProduced

def main():
    folderName = 'simulations'
    savePlotsFromSimulationsInFolder(folderName)
    createSinglePlotFromFilesInFolder(folderName)


if __name__ == '__main__':
    main()
