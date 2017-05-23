

class schedular: 

    def __init__(self):
        pass

    def order_tasks(self, listOfTasks):
        orderedTasks = []
        net = 0
        length = 0
        for task in listOfTasks:
            net += task.weight
            length += task.lengthInHours
        slope = net/length
        time = 0
        weight = 0
        tasksLeft = len(listOfTasks)
        while tasksLeft > 0:
            resultDelta = []
            for task in listOfTasks:
                resultDelta.append(abs(weight+task.weight-(time+task.lengthInHours)*slope))
            choice = resultDelta.index(min(resultDelta))
            time += listOfTasks[choice].lengthInHours
            weight += listOfTasks[choice].weight
            orderedTasks.append(listOfTasks[choice])
            listOfTasks.pop(choice)
            tasksLeft-=1
        return orderedTasks

    #TODO add break scheduling
    def scheduleBlock(self, timespan, startTime, tasksToSchedule, calendarID):
        while len(tasksToSchedule) > 0:
            if datetime.timedelta(minutes=tasksToSchedule[0].length+tasksToSchedule[0].setUp*2) < timespan:
                tasksToSchedule[0].schedule(startTime.date(), (startTime+datetime.timedelta(minutes=tasksToSchedule[0].setUp)).time(), calendarID)
                timespan -= datetime.timedelta(minutes=tasksToSchedule[0].length+tasksToSchedule[0].setUp*2)
                startTime += datetime.timedelta(minutes=tasksToSchedule[0].length+tasksToSchedule[0].setUp*2)
                tasksToSchedule.pop(0)
            else:
                #schedule breaks here
                return


    def schedule_day(self, googleEvents, tasksToSchedule, date, calendarID):
        i = 0
        while i < len(googleEvents)-1 and len(tasksToSchedule) != 0:
            nextBlock = googleEvents[i+1].start - googleEvents[i].end
            if(nextBlock > datetime.timedelta(minutes=tasksToSchedule[0].length+tasksToSchedule[0].setUp*2)):
                scheduleBlock(nextBlock, googleEvents[i].end, tasksToSchedule, calendarID)
            i += 1

