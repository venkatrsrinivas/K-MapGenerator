import copy
from forseti.formula import Symbol, Or, And, Not
from nose import runmodule
from nose.tools import assert_equal, assert_true
import util
from extra_formulas import GeneralizedAnd, GeneralizedOr


def test_helper():
    statement = Or(Or(Symbol("B"), Symbol("C")), Symbol("A"))
    new_statement, change = util.flatten(copy.deepcopy(statement))
    assert_equal(new_statement, GeneralizedOr(Symbol("B"), Symbol("C"), Symbol("A")))
    assert_true(change)


def test_helper2():
    statement = GeneralizedOr(Symbol("a"), Symbol("a"))
    # need to manually set it to this as otherwise the constructor would flatten it automatically
    statement.args[0] = Or(And(Symbol("b"), Not(Symbol("c"))), And(Symbol("c"), Not(Symbol("b"))))
    new_statement, change = util.flatten(copy.deepcopy(statement))
    assert_equal(new_statement, GeneralizedOr(Symbol("a"), And(Symbol("b"), Not(Symbol("c"))),
                                              And(Symbol("c"), Not(Symbol("b")))))
    assert_true(change)


def test_generalized_or_constructor():
    statement = GeneralizedOr(Or(Symbol("B"), Symbol("C")), Symbol("A"))
    assert_equal(statement, GeneralizedOr(Symbol("B"), Symbol("C"), Symbol("A")))

if __name__ == "__main__":
    runmodule()
