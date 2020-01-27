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

    print("Are the statements equivalent? " + str(equal))
    print("Statement 1 CDNF: " + str(parse1[0]))
    print("Statement 2 CDNF: " + str(parse2[0]))

generate_equivalency("A", "not(nots(A))") 