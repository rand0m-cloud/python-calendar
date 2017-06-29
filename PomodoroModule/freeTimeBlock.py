import datetime
from hunk import Hunk
from pomodoro import Pomodoro

class FreeTimeBlock:

    def __init__(self, startTime, endTime):
        self.startTime = startTime
        self.endTime = endTime
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
        self.OpenExtras = self.ExtraBlocks.__len__()

    def scheduleHunk(self, tasksToSchedule):
        pass

    def partialScheduleHunk(self, task):
        print "breaking hunk"
        for hunk in self.hunks:
            if hunk.partial and not hunk.filled:
                hunk.scheduleTask(task)
                return True
        for hunk in self.hunks:
            if not hunk.filled:
                hunk.scheduleTask(task)
                return True
        return False


    def scheduleExtra(self, task):
        scheduled = False
        for pomo in self.ExtraBlocks:
            if not pomo.filled:
                pomo.addTask(task)
                scheduled = True
                self.OpenExtras -= 1
                return True
        return scheduled

    def scheduleTask(self, task, length):
        print "Scheduling"
        for i in range(length):
            self.scheduleSingleTask(task)
        return True

    def scheduleSingleTask(self, task):

        print self.startTime
        if self.OpenExtras > 0:
            if self.scheduleExtra(task):
                self.OpenSpots -= 1
                return True
        if self.partialScheduleHunk(task):
            self.OpenSpots -= 1
            return True
        return False
    #push everthing to Google
    def finalizeBlock(self, google):
        for hunk in self.hunks:
            if hunk.filled:
                self.finalizeHunk(hunk,google)
            else:
                for i in range(hunk.scheduled):
                    self.finalizeTask(hunk.getTasks()[i],google)
        for pomo in self.ExtraBlocks:
            self.finalizeTask(pomo, google)
    def finalizeHunk(self, hunk, google):
        for task in hunk.getTasks():
            self.finalizeTask(task, google)
        self.startTime += datetime.timedelta(minutes=30)

    def finalizeTask(self, task, google):
        if task.filled:
            task.task.createGoogleEvent(self.startTime.date(), self.startTime.time(), 25, google)
            self.startTime += datetime.timedelta(minutes=30)
    def __str__(self):
        return str(self.startTime) + " : " + str(self.endTime) + " : " + str(self.OpenSpots)