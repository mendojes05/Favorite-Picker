class item:

    def __init__(self, item):
        self.name = item
        self.eliminators = []
        self.eliminated = False            


    #method to set when eliminated
    def elim(self, item):
        self.eliminated = True
        self.eliminators.append(item)