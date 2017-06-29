from freeTimeBlock import FreeTimeBlock

class PomodoroScheduler:

    def __init__(self, events, start, end):
        self.freetime = self.determineFreetime(events, start, end)
        self.maxTasks = 0
        for block in self.freetime:
            self.maxTasks += block.OpenSpots
        print self.maxTasks




    def scheduleTasks(self, tasks, google):
        for task in tasks:
            scheduled = False
            for block in self.freetime:
                if block.OpenSpots >= task.length:
                    scheduled = block.scheduleTask(task, task.length)
                    if scheduled:
                        break
            if not scheduled:
                print "Could not schedule task"
                print task
        for block in self.freetime:
            block.finalizeBlock(google)

    def determineFreetime(self, events, start, end):
        FreeTime = []

        endTime = None
        for event in events:
            if event.start > start :
                startTime = event.start
                if startTime > end:
                    startTime = end
                if endTime is not None:
                    delta = startTime - endTime
                    if delta.days >= 0 and delta.seconds > 0:
                        FreeTime.append(FreeTimeBlock(endTime, startTime))
                endTime = event.end
                if endTime > end:
                    break
        for block in FreeTime:
            print block
        return FreeTime