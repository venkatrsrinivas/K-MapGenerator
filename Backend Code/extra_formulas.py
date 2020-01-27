# -*- coding: utf-8 -*-
"""
These should be moved into the main forseti package most likely as they are useful
in a variety of contexts
"""
from copy import deepcopy
from forseti.formula import Formula, LogicalOperator, And, Or


class GeneralizedAnd(LogicalOperator):
    def __init__(self, *kwargs):
        if len(kwargs) < 2:
            raise Exception("Need to have at least 2 arguments")
        super(GeneralizedAnd, self).__init__(*kwargs)
        for kwarg in kwargs:
            if isinstance(kwarg, And) or isinstance(kwarg, GeneralizedAnd):
                for arg in kwarg.args:
                    self.args.append(arg)
            else:
                self.args.append(kwarg)

    def __repr__(self):
        return "and(" + ", ".join([repr(arg) for arg in self.args]) + ")"

    def __str__(self):
        return "(" + " & ".join([str(arg) for arg in self.args]) + ")"

    def __eq__(self, other):
        if not isinstance(other, GeneralizedAnd):
            return False
        test = deepcopy(self.args)
        i = 0
        while i < len(test):
            for j in other.args:
                if j == test[i]:
                    del test[i]
                    i -= 1
                    break
            i += 1
        return len(test) == 0

    def __lt__(self, other):
        if not isinstance(other, GeneralizedAnd):
            raise TypeError("Can only compare GeneralizedAnd together. Got type '%s'." % type(other))

        if len(self.args) < len(other.args):
            return True
        elif len(self.args) > len(other.args):
            return False
        else:
            i = 0
            while i < len(self.args):
                if self.args[i] < other.args[i]:
                    return True
                elif other.args[i] < self.args[i]:
                    return False
                i += 1
        return True

    def __gt__(self, other):
        if not isinstance(other, GeneralizedAnd):
            raise TypeError("Can only compare GeneralizedAnd together. Got type '%s'." % type(other))

        if len(self.args) < len(other.args):
            return True
        elif len(self.args) > len(other.args):
            return False
        else:
            i = 0
            while i < len(self.args):
                if self.args[i] > other.args[i]:
                    return True
                i += 1
        return False


class GeneralizedOr(LogicalOperator):
    def __init__(self, *kwargs):
        if len(kwargs) < 2:
            raise Exception("Need to have at least 2 arguments")
        super(GeneralizedOr, self).__init__(*kwargs)
        for kwarg in kwargs:
            if isinstance(kwarg, Or) or isinstance(kwarg, GeneralizedOr):
                for arg in kwarg.args:
                    self.args.append(arg)
            else:
                self.args.append(kwarg)

    def __repr__(self):
        return "or(" + ", ".join([repr(arg) for arg in self.args]) + ")"

    def __str__(self):
        return "(" + " | ".join([str(arg) for arg in self.args]) + ")"


class Contradiction(Formula):
    def __init__(self):
        super(Contradiction, self).__init__()

    def __repr__(self):
        return "FALSE"

    def __str__(self):
        return "⊥"

    def __eq__(self, other):
        if isinstance(other, Contradiction):
            return True
        else:
            return False

    def __ne__(self, other):
        return not (self == other)

    def __gt__(self, other):
        return False

    def __ge__(self, other):
        pass

    def __lt__(self, other):
        pass

    def __le__(self, other):
        pass


class Tautology(Formula):
    def __init__(self):
        super(Tautology, self).__init__()

    def __repr__(self):
        return "TRUE"

    def __str__(self):
        return "T"

    def __eq__(self, other):
        if isinstance(other, Contradiction):
            return True
        else:
            return False

    def __ne__(self, other):
        return not (self == other)

    def __gt__(self, other):
        return False

    def __ge__(self, other):
        pass

    def __lt__(self, other):
        pass

    def __le__(self, other):
        pass
