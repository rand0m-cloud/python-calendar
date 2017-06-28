from pomodoro import Pomodoro

class Hunk:

    def __init__(self):
        self.tasks = []
        self.tasks.append(Pomodoro())
        self.tasks.append(Pomodoro())
        self.tasks.append(Pomodoro())
        self.tasks.append(Pomodoro())
        self.partial = False
        self.filled = False
        self.scheduled = 0

    def scheduleTask(self, task):
        self.partial = True
        for pomo in self.tasks:
            if not pomo.filled:
                pomo.addTask(task)
                self.scheduled += 1
                if self.scheduled == 4:
                    self.filled = True
                return True
        self.filled = True
        return False