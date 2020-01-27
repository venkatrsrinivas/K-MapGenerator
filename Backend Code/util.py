# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from copy import deepcopy

from forseti.formula import Symbol, Predicate, Not, And, Or, Iff, If
from extra_formulas import GeneralizedAnd, GeneralizedOr, Contradiction, Tautology


class StepTypes(object):
    START = 0
    IFF = 1
    IF = 2
    NOT = 3
    AND = 4
    ADJACENCY = 5
    FLATTEN = 6
    IDEMPOTENCE_CONJUNCT = 7
    ANNIHILATION = 8
    COMMUTATION = 9
    IDEMPOTENCE_DISJUNCT = 10

    @classmethod
    def get_message(cls, step_type):
        if step_type == cls.START:
            return "Starting Formula"
        elif step_type == cls.IFF:
            return "Convert Iff"
        elif step_type == cls.IF:
            return "Convert If"
        elif step_type == cls.NOT:
            return "Distribute Not"
        elif step_type == cls.AND:
            return "Distribute And"
        elif step_type == cls.ADJACENCY:
            return "Perform Adjacency"
        elif step_type == cls.FLATTEN:
            return "Perform Association"
        elif step_type == cls.IDEMPOTENCE_CONJUNCT:
            return "Performed Idempotence on Conjuncts"
        elif step_type == cls.ANNIHILATION:
            return "Performed Complement and Annihilation"
        elif step_type == cls.COMMUTATION:
            return "Performed Commutation"
        elif step_type == cls.IDEMPOTENCE_DISJUNCT:
            return "Performed Idempotence on Disjuncts"
        else:
            return "Unknown type"


def convert(statement):
    symbols = list()
    get_symbols(statement, symbols)
    step_list = list()
    step_list.append([[deepcopy(statement)], StepTypes.START])

    steps = [[convert_iff, StepTypes.IFF], [convert_if, StepTypes.IF], [distribute_not, StepTypes.NOT],
             [flatten, StepTypes.FLATTEN], [distribute_and, StepTypes.AND], [flatten, StepTypes.FLATTEN],
             [perform_adjacency, StepTypes.ADJACENCY], [flatten, StepTypes.FLATTEN],
             [perform_commutation, StepTypes.COMMUTATION],
             [perform_idempotence_conjuncts, StepTypes.IDEMPOTENCE_CONJUNCT],
             [perform_annihilation, StepTypes.ANNIHILATION],
             [perform_idempotence_disjuncts, StepTypes.IDEMPOTENCE_DISJUNCT],
             [perform_commutation_disjuncts, StepTypes.COMMUTATION]]
    for step in steps:
        statement, step_list = _run_change(statement, symbols, step_list, step[0], step[1])

    return statement, step_list


def _run_change(statement, symbol_list, step_list, function, step_type):
    changed = True
    this_step = []
    while changed is True:
        if function == perform_adjacency:
            statement, changed = function(statement, symbol_list)
        else:
            statement, changed = function(statement)
        if changed:
            this_step.append(deepcopy(statement))

    if len(this_step) > 0:
        step_list.append([this_step, step_type])

    return statement, step_list


def get_symbols(statement, symbols_list):
    if isinstance(statement, Symbol):
        symbols_list.append(statement)
    else:
        for arg in statement.args:
            get_symbols(arg, symbols_list)


def convert_iff(statement):
    """
    Convert biconditionals into two conditionals joined by an And

    :param statement:
    :return:
    """
    if isinstance(statement, Symbol):
        return statement, False

    change = False
    args = statement.args
    for i in range(len(args)):
        args[i], change = convert_iff(args[i])
        if change is True:
            break

    if change is False and isinstance(statement, Iff):
        statement = GeneralizedAnd(If(deepcopy(args[0]), deepcopy(args[1])), If(deepcopy(args[1]), deepcopy(args[0])))
        change = True

    return statement, change


def convert_if(statement):
    """
    Convert conditional (A -> B) into (~A or B)

    :param statement:
    :return:
    """
    if isinstance(statement, Symbol) or isinstance(statement, Not):
        return statement, False

    change = False
    args = statement.args
    for i in range(len(args)):
        args[i], change = convert_if(args[i])
        if change is True:
            break

    if change is False and isinstance(statement, If):
        statement = GeneralizedOr(Not(deepcopy(args[0])), deepcopy(args[1]))
        change = True

    return statement, change


def distribute_not(statement):
    """
    Distribute not over and/or clauses (flipping them)

    :param statement:
    :return:
    """
    if isinstance(statement, Symbol):
        return statement, False

    args = statement.args
    change = False
    if isinstance(statement, Not):
        if isinstance(args[0], And) or isinstance(args[0], Or) \
                or isinstance(args[0], GeneralizedOr) or isinstance(args[0], GeneralizedAnd):
            new_type = GeneralizedOr
            if isinstance(args[0], Or) or isinstance(args[0], GeneralizedOr):
                new_type = GeneralizedAnd
            new_args = []
            for arg in args[0].args:
                new_args.append(Not(arg))
            statement = new_type(*new_args)
            change = True
        elif isinstance(args[0], Not):
            statement = args[0].args[0]
            change = True
        """
        elif isinstance(args[0], Quantifier):
            new_type = Existential
            if isinstance(args[0], Existential):
                new_type = Universal
            statement = new_type(args[0].symbol, Not(args[0].args[0]))
            statement.args[0] = _distribute_not(statement.args[0])
        """
    else:
        for i in range(len(args)):
            args[i], change = distribute_not(args[i])
            if change:
                break
    return statement, change


def distribute_and(statement):
    """
    Distribute or over any nested and statements (so and becomes
    outer most logical operator)

    :param statement:
    :return:
    """
    if is_atomic(statement):
        return statement, False

    change = False
    args = statement.args
    if isinstance(statement, And) or isinstance(statement, GeneralizedAnd):
        for i in range(len(args)):
            if isinstance(args[i], Or) or isinstance(args[i], GeneralizedOr):
                # distribute args[j] over args[i]
                j = i-1 if i > 0 else 1
                new_args = []
                for k in range(len(args[i].args)):
                    new_args.append(GeneralizedAnd(args[i].args[k], args[j]))

                if len(args) == 2:
                    statement = GeneralizedOr(*new_args)
                else:
                    args[min(i, j)] = GeneralizedOr(*new_args)
                    del args[max(i, j)]
                change = True
                if change:
                    return statement, change
                break

    args = statement.args
    for i in range(len(args)):
        args[i], change = distribute_and(args[i])
        if change:
            break

    return statement, change


def flatten(statement):
    statement, change1 = _flatten_helper(statement, GeneralizedAnd, And)
    statement, change2 = _flatten_helper(statement, GeneralizedOr, Or)
    return statement, (change1 or change2)


def _flatten_helper(statement, generalized_type, other_type):
    if is_atomic(statement):
        return statement, False

    change = False
    args = statement.args
    if isinstance(statement, other_type):
        statement = generalized_type(*statement.args)
        change = True

    if isinstance(statement, generalized_type):
        for i in range(len(args)):
            if isinstance(args[i], other_type):
                args[i] = generalized_type(*args[i].args)
            if isinstance(args[i], generalized_type):
                args[i], _ = _flatten_helper(args[i], generalized_type, other_type)
                for arg in args[i].args:
                    args.append(arg)
                del args[i]
                change = True
    else:
        for i in range(len(args)):
            args[i], change = _flatten_helper(args[i], generalized_type, other_type)
    return statement, change


def perform_adjacency(statement, symbols):
    change = False
    if is_atomic(statement):
        test = statement
        if isinstance(statement, Not):
            test = statement.args[0]
        if len(symbols) == 1:
            return statement, change
        else:
            not_symbols = deepcopy(symbols)
            i = 0
            for i in range(len(not_symbols)):
                if not_symbols[i] == test:
                    del not_symbols[i]
                    break
            new_symbols = _adjacency_helper(not_symbols)
            or_args = []
            for i in new_symbols:
                args = [statement]
                for j in i:
                    args.append(j)
                or_args.append(GeneralizedAnd(*args))
            statement = GeneralizedOr(*or_args)
            change = True
    elif isinstance(statement, GeneralizedOr):
        for i in range(len(statement.args)):
            statement.args[i], change_new = perform_adjacency(statement.args[i], symbols)
            change = (change_new or change)
    elif isinstance(statement, GeneralizedAnd):
        test = []
        for i in statement.args:
            if isinstance(i, Not):
                if i.args[0] not in test:
                    test.append(i.args[0])
            else:
                if i not in test:
                    test.append(i)

        if len(symbols) == 1 or len(symbols) == len(test):
            return statement, change
        else:
            not_symbols = deepcopy(symbols)
            i = 0
            while i < len(not_symbols):
                j = 0
                while j < len(test):
                    if not_symbols[i] == test[j]:
                        del not_symbols[i]
                        i -= 1
                        break
                    j += 1
                i += 1
            if len(not_symbols) > 0:
                new_symbols = _adjacency_helper(not_symbols)
                or_args = []
                for i in new_symbols:
                    args = deepcopy(statement.args)
                    for j in i:
                        args.append(j)
                    or_args.append(GeneralizedAnd(*args))
                statement = GeneralizedOr(*or_args)
                change = True

    return statement, change


def _adjacency_helper(symbols):
    return_list = []
    """
    [a, b, c]
    [[a, b, c], [a, b, ~c], [a, ~b, c], ...]
    """
    for i in symbols:
        if len(return_list) == 0:
            return_list.append([i])
            return_list.append([Not(i)])
        else:
            temp = deepcopy(return_list)
            for j in range(len(return_list)):
                return_list[j].append(i)
            for j in range(len(temp)):
                return_list.append(temp[j] + [Not(i)])
    return return_list


def perform_commutation(statement):
    change = False
    if isinstance(statement, GeneralizedOr):
        for i in range(len(statement.args)):
            statement.args[i], change_new = perform_commutation(statement.args[i])
            change = (change_new or change)
    elif isinstance(statement, GeneralizedAnd):
        new = sorted(statement.args)
        if new != statement.args:
            statement.args = new
            change = True
    return statement, change


def perform_idempotence_conjuncts(statement):
    """
    I don't expect anything outside of Symbol, GeneralizedAnd, or GeneralizedOr to come into
    this function as it really should only be run after the other functions within this process

    :param statement:
    :return:
    """
    change = False
    if isinstance(statement, GeneralizedOr):
        for i in range(len(statement.args)):
            statement.args[i], change_new = perform_idempotence_conjuncts(statement.args[i])
            change = (change_new or change)
    elif isinstance(statement, GeneralizedAnd):
        i = 0
        while i < (len(statement.args)-1):
            j = i+1
            while j < len(statement.args):
                if statement.args[i] == statement.args[j]:
                    del statement.args[j]
                    change = True
                    j -= 1
                j += 1
            i += 1

    return statement, change


def perform_annihilation(statement):
    change = False
    if isinstance(statement, GeneralizedOr):
        i = 0
        while i < len(statement.args):
            statement.args[i], change_new = perform_annihilation(statement.args[i])
            if isinstance(statement.args[i], Contradiction):
                del statement.args[i]
                i -= 1
            i += 1
            change = (change_new or change)
        if len(statement.args) == 0:
            return Contradiction(), True
    elif isinstance(statement, GeneralizedAnd):
        i = 0
        while i < (len(statement.args)-1):
            if isinstance(statement.args[i], Not):
                negate = statement.args[i].args[0]
            else:
                negate = Not(statement.args[i])
            j = i + 1
            while j < len(statement.args):
                if negate == statement.args[j]:
                    return Contradiction(), True
                j += 1
            i += 1
    return statement, change


def perform_idempotence_disjuncts(statement):
    change = False
    if isinstance(statement, GeneralizedOr):
        i = 0
        while i < len(statement.args):
            j = i + 1
            while j < len(statement.args):
                if statement.args[i] == statement.args[j]:
                    change = True
                    del statement.args[j]
                    j -= 1
                j += 1
            i += 1
    return statement, change


def perform_commutation_disjuncts(statement):
    change = False
    if isinstance(statement, GeneralizedOr):
        new = sorted(statement.args)
        if new != statement.args:
            statement.args = new
            change = True
    return statement, change


def is_atomic(statement):
    return isinstance(statement, Symbol) or isinstance(statement, Predicate) or \
           isinstance(statement, Tautology) or isinstance(statement, Contradiction) or isinstance(statement, Not)


def pretty_print(formula, depth=0):
    """

    :param formula:
    :param depth:
    :return:
    """
    if isinstance(formula, Symbol) or isinstance(formula, Predicate) \
            or isinstance(formula, Contradiction) or isinstance(formula, Tautology):
        text = str(formula)
    elif isinstance(formula, Not):
        text = "¬" + pretty_print(formula.args[0], depth=depth+1)
    else:
        temp = []
        for arg in formula.args:
            temp.append(pretty_print(arg, depth=depth+1))
        if isinstance(formula, And) or isinstance(formula, GeneralizedAnd):
            text = " ∧ ".join(temp)
        elif isinstance(formula, Or) or isinstance(formula, GeneralizedOr):
            text = " ∨ ".join(temp)
        elif isinstance(formula, If):
            text = " → ".join(temp)
        elif isinstance(formula, Iff):
            text = " ↔ ".join(temp)
        else:
            raise TypeError("Invalid Formula Type: " + str(type(formula)))
        if depth > 0:
            text = "(" + text + ")"
    return text.strip()
