from abc import ABCMeta


class AbstractPoll(object):
    __metaclass__ = ABCMeta

    def __init__(self, condidates):
        pass

    def account_votes(self, votes):
        pass

    def participation(self):
        pass

    @property
    def winner(self):
        pass

    @property
    def result(self):
        pass
    



class ClassicPoll(AbstractPoll):

    def __init__(self, candidates):
        self.stats = {}
        for c in candidates:
            self.stats[c] = 0



    def account_votes(self, data_votes):
        for v in data_votes:
            self.stats[v.candidate] += 1

    @property
    def winner(self):
        return sorted(self.stats.keys(), key=lambda c: self.stats[c])[0]

