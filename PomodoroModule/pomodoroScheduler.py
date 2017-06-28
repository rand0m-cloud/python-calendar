from freeTimeBlock import FreeTimeBlock

class PomodoroScheduler:

    def __init__(self, events):
        self.freetime = self.determineFreetime(events)




    def scheduleTasks(self, tasks):
        for task in tasks:
            scheduled = False
            for block in self.freetime:
                if block.OpenSpots > 0:
                    scheduled = block.scheduleTask(task)
                    if scheduled:
                        break
            if not scheduled:
                print "Could not schedule task"
                print task

    def determineFreetime(self, events):
        FreeTime = []

        endTime = None
        for event in events:
            startTime = event.start
            if endTime is not None:
                delta = startTime - endTime
                if delta.days >= 0 and delta.seconds > 0:
                    FreeTime.append(FreeTimeBlock(endTime, startTime))
            endTime = event.end

        return FreeTime