
class Pomodoro:
    def __init__(self):
        self.filled = False

    def addTask(self, task):
        print "adding"
        print task
        self.filled = True