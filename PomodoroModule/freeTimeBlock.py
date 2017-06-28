import datetime
from hunk import Hunk
from pomodoro import Pomodoro

class FreeTimeBlock:

    def __init__(self, startTime, endTime):
        timeDelta = endTime - startTime

        if(timeDelta.days >= 0):
            self.length = timeDelta.seconds / 60.0
        else:
            self.length = 0

        numOfHunks = int(self.length)/145
        self.hunks = []
        for i in range(numOfHunks):
            self.hunks.append(Hunk())
        remainingTime = int(self.length)%145
        self.ExtraBlocks = []
        if remainingTime >= 30:
            self.ExtraBlocks.append(Pomodoro())
        if remainingTime >= 60:
            self.ExtraBlocks.append(Pomodoro())
        if remainingTime >= 90:
            self.ExtraBlocks.append(Pomodoro())

        self.OpenSpots = self.hunks.__len__()*4 + self.ExtraBlocks.__len__()
        self.OpenHunks = self.hunks.__len__()

    def scheduleHunk(self, tasksToSchedule):
        pass

    def scheduleTask(self, task):
        pass

    def finalizeBlock(self):
        pass