from unitgrade import hide, UTestCase
from exam_generator.exam import Question, jinjafy
from types import SimpleNamespace
import gym
import numpy as np
import sympy as sym
import os
import inspect
from unitgrade import NotebookTestCase
from exam_generator.mat1.mat1exam import QuestionController, Mat1Question

# class Mat1Question(NotebookTestCase, Question):
#     notebook = None
#     sheet = None
#
#     def __init__(self, *args, seed=1, **kwargs):
#         # set up parts of the environment.
#         Question.__init__(self, seed=seed)
#         UTestCase.__init__(self, *args, **kwargs)
#
#     def render(self, exam):
#         # Use the exam
#         self.dirs = exam.get_dirs()
#
#         if not os.path.isdir(self.dirs.generated):
#             os.makedirs(self.dirs.generated)
#         if not os.path.isdir(self.dirs.figures):
#             os.makedirs(self.dirs.figures)
#
#         # Now it is appropriate for the great jinja.
#         np.random.seed(self.seed)
#         x = self.generate()
#         if not isinstance(x, dict):
#             x = x.__dict__
#         x = {**x, **self._extra_generation(exam)}
#
#         x['overall_exam_score'] = self.overall_exam_score
#         x['question_title'] = self.question_title
#         x['clearpage'] = self.clearpage
#         x['include_solution_box'] = self.include_solution_box
#
#         dn = os.path.basename(os.path.dirname(inspect.getfile(self.__class__)))
#         texfile = os.path.dirname(inspect.getfile(self.__class__)) + "/" + os.path.basename(
#             inspect.getfile(self.__class__))[:-3] + ".tex"
#
#         # What should it do?
#         # Render the question and return it as a str.
#         # from
#         s = jinjafy(self.dirs, self.sheet, x)
#         return s
#
#     def name(self):
#         return f"{self.__class__.__name__}_{self.seed}"
#
#     def render_dummy(self, r):
#         # Simplest?
#         # Make an exam and deploy to dummy file?
#         from exam_generator.mat1.mat1exam import Mat1Exam
#         class DummyExam(Mat1Exam):
#             r = 23
#             pass
#         ex = DummyExam()
#         s = self.render(ex)
#         with open("./homework.md", 'w') as f:
#             f.write(s.strip())
#         from exam_generator.mat1.mat1exam import jupytext_file
#         jupytext_file("./homework.md")

class VerificationQuestion(Mat1Question):
    # throw_error_on_no_tex_file = False
    notebook = 'homework.ipynb'
    sheet = """
# Hand-in code

The handin code will be written on the blackboard by the TA near the end of the test. Simply write the handin code below
(as a string) to confirm that you handed in during the test. When done, take a selfie of yourself and the handin code as a reciept, in case the 
handin code was mis-typed. 

```{code-cell} ipython3
handin_code = 'c000000'  # Write the handin code here. It has the format 'c123456789'.
handin_code = '{{handin_code}}' #!b;silent #!b
handin_code_checksum = sum([int(i) for i in handin_code[1:]])
if handin_code_checksum != {{handin_code_checksum}}:
    print("You specified the wrong handin code. Please ask the TA")
else:
    import subprocess, sys
    if "-nograde" not in sys.argv:
        subprocess.run(["cd ../../../ && python -m {{grade_script}} --noprogress --brief"], shell=True)        
```
"""
    def test_handin_code_checksum(self):
        self.assertEqualC(self.nb.handin_code_checksum)

    @hide
    def test_handin_code_checksum_hidden(self):
        self.assertEqualC(self.nb.handin_code_checksum)

    @hide
    def test_handin_code_hidden(self):
        self.assertEqualC(self.nb.handin_code)

    def generate(self):
        x = SimpleNamespace()
        x.a = 1+np.random.randint(100)
        x.b = 1+np.random.randint(100)
        print(self.question_args)
        print(self.dirs)
        x.handin_code = self.question_args['code']
        x.handin_code_checksum = sum([int(i) for i in x.handin_code[1:]])
        x.grade_script = f"{os.path.relpath(self.dirs.code, self.dirs.package_base).replace('/', '.')}.{self.exam.name}_grade"
        return x

class VerificationQuestionController(QuestionController):
    questions = [VerificationQuestion]



if __name__ == "__main__":
    # q = DP01(seed=3)
    # q.render_dummy(r = 3)
    # import unittest
    # unittest.main()
    pass