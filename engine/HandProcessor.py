
class HandProcessor:
    def __init__(self, handMap):
        self.handMap = handMap

    def process(self):
        pass

    def isHandStone(self):
        raise NotImplementedError

    def isHandPaper(self):
        raise NotImplementedError

    def isHandScissors(self):
        raise NotImplementedError