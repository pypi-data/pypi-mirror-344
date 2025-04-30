import os.path

from exam_generator.exam import Question, MCQuestion
from types import SimpleNamespace
import numpy as np

def uroll(bank):
    options = {'true': [], 'false': []}
    # ft = []
    # tt = []
    for k in bank:
        if k in ['true', 'false']:
            options[k] += bank[k]
        else:
            t, f = uroll(bank[k])
            options['true'] += t
            options['false'] += f
    return options['true'], options['false']


# class ManualMultipleChoice(MCQuestion):
#     def __init__(self, seed, bank, title='', template_base='explicit_question'):
#         super().__init__(seed, title=title)
#         self.template_base = template_base
#         self.bank = bank
#
#     def render(self, exam):
#         dirs = exam.get_dirs()
#         if not os.path.isfile(dirs.base + "/" + self.solution_file):
#             with open(dirs.base + "/" + self.solution_file, 'w') as f:
#                 f.write("Put your solution in " + self.solution_file)
#
#         return super().render(exam)
#
#     def generate(self):
#         x = SimpleNamespace()
#         # from numpy.random
#         itrue, ifalse = uroll(self.bank)
#
#         f = list(np.random.choice(ifalse, size=3, replace=False))
#         t = np.random.choice(itrue, size=1, replace=False)[0]
#         x.answers = [t] + f
#         x.static_solution = "statcic/"+self.solution_file
#
#         return x
#
#     pass

class RandomMultipleChoice(MCQuestion):

    def __init__(self, seed, bank, title='', solution_file='sol1.tex'):
        super().__init__(seed, title=title)
        self.solution_file = solution_file
        self.bank = bank

    def render(self, exam):
        dirs = exam.get_dirs()
        if not os.path.isfile(dirs.base + "/" + self.solution_file):
            with open(dirs.base + "/" + self.solution_file, 'w') as f:
                f.write("Put your solution in " + self.solution_file)

        return super().render(exam)

    def generate(self):
        x = SimpleNamespace()
        # from numpy.random
        itrue, ifalse = uroll(self.bank)

        f = list(np.random.choice(ifalse, size=3, replace=False))
        t = np.random.choice(itrue, size=1, replace=False)[0]
        x.answers = [t] + f
        x.static_solution = self.solution_file

        return x

