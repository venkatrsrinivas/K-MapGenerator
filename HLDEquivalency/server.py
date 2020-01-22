from __future__ import unicode_literals
from flask import Flask, Markup, render_template, request
import logical_equivalency
import util

FLASK_APP = Flask(__name__)


@FLASK_APP.route("/")
def index_page():
    return render_template('index.html')


@FLASK_APP.route("/submit", methods=['POST'])
def generate_equivalency():
    formula1 = request.form['formula1']
    formula2 = request.form['formula2']
    form = Markup(render_template('form.html', formula1=formula1, formula2=formula2))

    try:
        equal, parse1, parse2 = logical_equivalency.runner(formula1, formula2)
    except (SyntaxError, TypeError) as exception:
        return render_template('error.html', error=str(exception), form=form)

    final_steps1 = []
    for steps, step_type in parse1[1]:
        final_steps1.append([util.pretty_print(steps[-1]), steps[:-1], util.StepTypes.get_message(step_type)])

    final_steps2 = []
    for steps, step_type in parse2[1]:
        final_steps2.append([util.pretty_print(steps[-1]), steps[:-1], util.StepTypes.get_message(step_type)])

    return render_template('show.html', equal=equal, form=form, steps1=final_steps1, final_form1=parse1[0],
                           steps2=final_steps2, final_form2=parse2[0])


if __name__ == '__main__':
    FLASK_APP.debug = True
    FLASK_APP.run()
