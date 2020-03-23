# This file is from HLD-Equivalency
from __future__ import unicode_literals
import logical_equivalency
import util

def generate_equivalency(formula1, formula2):
    try:
        equal, parse1, parse2 = logical_equivalency.runner(formula1, formula2)
    except (SyntaxError, TypeError) as exception:
        print(str(exception))
        exit()

    final_steps1 = []
    for steps, step_type in parse1[1]:
        final_steps1.append([util.pretty_print(steps[-1]), steps[:-1], util.StepTypes.get_message(step_type)])

    final_steps2 = []
    for steps, step_type in parse2[1]:
        final_steps2.append([util.pretty_print(steps[-1]), steps[:-1], util.StepTypes.get_message(step_type)])

    return (equal, str(parse1[0]), str(parse2[0]), parse1[2], parse2[2]) 
    #Return 5 things: Boolean (True if formula1 is equivalent to formula2, False otherwise), 
    #Two Strings (Two CDNF Formulas)
    #Two Booleans (Indicating If Either Formula Is Contradiction)

