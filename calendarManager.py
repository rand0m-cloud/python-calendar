from googleEvent import googleEvent
from unscheduledTask import *


def parse_tasks(listOfTasks):
    tasksToSchedule = []

    for task in listOfTasks:

        print task
        title = task["title"].split('#')
        if len(title) == 1:
            continue
       # change_task_name(task, title[0])
        # number - length, s-number of segements, r-repeat frequency, p-preparation time
        length = 0
        fun = 0
        repeatsFreq = 0 #TODO Add me
        segments = 1
        prep = 0
        for bit in title:
            bit = bit.strip()
            if bit.isdigit():
                length = int(bit)
            if bit.startswith("s"):
                segments = int(bit[1:])
            if bit.startswith("r"):
                repeatsFreq = int(bit[1:])
            if bit.startswith("p"):
                prep = int(bit[1:])
            if bit.startswith("i"):
                fun = int(bit[1:])
        length /= segments
        while segments>0:
            tasksToSchedule.append(unscheduledTask(title[0].strip(), length, fun, setUp=prep))
            segments-=1
    return tasksToSchedule


def order_tasks(listOfTasks):
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
def scheduleBlock(timespan, startTime, tasksToSchedule, calendarID):
    while len(tasksToSchedule) > 0:
        if datetime.timedelta(minutes=tasksToSchedule[0].length+tasksToSchedule[0].setUp*2) < timespan:
            tasksToSchedule[0].schedule(startTime.date(), (startTime+datetime.timedelta(minutes=tasksToSchedule[0].setUp)).time(), calendarID)
            timespan -= datetime.timedelta(minutes=tasksToSchedule[0].length+tasksToSchedule[0].setUp*2)
            startTime += datetime.timedelta(minutes=tasksToSchedule[0].length+tasksToSchedule[0].setUp*2)
            tasksToSchedule.pop(0)
        else:
            #schedule breaks here
            return


def schedule_day(googleEvents, tasksToSchedule, date, calendarID):
    startTime = datetime.datetime.combine(date, datetime.time(hour=8))
    i = 0
    while i < len(googleEvents)-1 and len(tasksToSchedule) != 0:
        nextBlock = googleEvents[i+1].start - googleEvents[i].end
        if(nextBlock > datetime.timedelta(minutes=tasksToSchedule[0].length+tasksToSchedule[0].setUp*2)):
            scheduleBlock(nextBlock, googleEvents[i].end, tasksToSchedule, calendarID)
        i += 1


def main():
    calendarID = select_calendar()

    events = get_events(calendarID)

    cleanEvents = [] #exclude all day events

    for event in events:
        if event["start"].has_key("dateTime")==False:
                continue
        calEvent = googleEvent(event)
        cleanEvents.append(calEvent)
        print calEvent


    listID = select_list()

    listOfTasks = get_tasks(listID)

    taskToSchedule = parse_tasks(listOfTasks)

    taskToSchedule = order_tasks(taskToSchedule)

    for task in taskToSchedule:
        print task

    schedule_day(cleanEvents, taskToSchedule, datetime.date.today()+datetime.timedelta(days=1), calendarID)


if __name__ == '__main__':
    main()

