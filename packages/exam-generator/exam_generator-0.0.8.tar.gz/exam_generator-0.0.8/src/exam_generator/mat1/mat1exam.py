from unitgrade import hide, UTestCase
from exam_generator.exam import Question, jinjafy
import numpy as np
import os
import inspect
from unitgrade import NotebookTestCase
from exam_generator.exam import Exam
import subprocess

JUPYTER_HEAD = """
---
jupytext:
  formats: ipynb,.pct.py:percent,.lgt.py:light,.spx.py:sphinx,md,Rmd,.pandoc.md:pandoc,.myst.md:myst
  text_representation:
    extension: '.md'
    format_name: myst
    format_version: '0.7'
    jupytext_version: 1.4.0+dev
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---
""".strip()

def get_jupyter_head(title='untitled document'):
    JUPYTER_HEAD = f"""
---
jupytext:
  formats: ipynb,.pct.py:percent,.lgt.py:light,.spx.py:sphinx,md,Rmd,.pandoc.md:pandoc,.myst.md:myst
  text_representation:
    extension: '.md'
    format_name: myst
    format_version: '0.7'
    jupytext_version: 1.4.0+dev
kernelspec:
  display_name: Python 3
  language: python
  name: python3
title: '{title}'
---
    """.strip()
    return JUPYTER_HEAD
    pass

class Mat1Exam(Exam):
    title = "Untiled problem set"

    def _get_base_location(self):
        base = os.path.dirname(inspect.getfile(self.__class__))
        return base

    def get_dirs(self):
        d = super().get_dirs()
        d.code = f"{d.code}_{self.seed}"
        if not os.path.isdir(d.code):
            os.makedirs(d.code)
        d.package_base = d.base +"/src"
        return d

    def render(self):
        def bracket(s):
            return "{"+ s+"}"
        # Take each question. Render it to an output directory. Then
        dirs = self.get_dirs()
        # qpath = []

        # questions = self.questions[0]['questions']
        # Resolve this to specific questions.

        qq = {}
        qq['questions'] = {}
        np.random.seed(self.seed)

        for k, q in self.questions.items():
            qq = self.questions[k]['question']
            self.questions[k]['variant'] = qq.questions[np.random.randint(len(qq.questions))]

        mb_base = """
{{JUPYTER_HEAD}}

{% for q in questions %}
{{q.md}}
{% endfor %}
        """.strip()

        x = {'mds': []}
        x['title'] = self.title
        x['JUPYTER_HEAD'] = get_jupyter_head(title=self.title)

        a =2
        for q in self.questions.values():
            # print("init", q)
            # if isinstance(q['question'], QuestionController):
            qv = q['variant'](seed=self.seed, question_args=q['question'].question_args)
            # else:
            #     qv = q['variant']

            # print("Didd init")
            x['mds'].append(qv.render(self))
            q['md'] = qv.render(self)

        x['questions'] = list(self.questions.values())
        md = jinjafy(dirs, mb_base, x)

        md_out = f"{dirs.code}/{self.name}.md"
        with open(md_out, "w") as f:
            f.write(md.strip())

        jupytext_file(md_out)

        def get_source(qq):
            source = []
            for k, v in qq.__dict__.items():
                if k not in ['sheet', 'generate', '__module__', '__annotations__', '__init__', 'build_md', 'name', 'notebook']:
                    print(k)
                    print(k, qq.__dict__[k])
                    if isinstance(qq.__dict__[k], bool) or v is None or isinstance(v, dict):
                        continue
                    s = inspect.getsource(qq.__dict__[k])
                    source.append(s)
            return source

        js = """
class Question{{n}}(NotebookTestCase):
    notebook = "{{notebook}}"
    
    {% for f in functions %}
{{f}}
    {% endfor %}    
"""
        qnames = []
        qs = []
        notebook = md_out[:-2] + "ipynb"
        for k, q in self.questions.items():
            functions = get_source(q['variant'])

            x = dict(notebook=os.path.basename(notebook), functions=functions, n=k + 1)
            qs.append( jinjafy(dirs, js, x))
            qnames.append(f"Question{k+1}")


        fulldoc = """
from unitgrade import hide, UTestCase
from unitgrade import UTestCase, Report
# from exam_generator.exam import Question, jinjafy
from types import SimpleNamespace
# import gym
import numpy as np
import sympy as sym
import os
import inspect
from unitgrade import NotebookTestCase

{% for q in qs %}
{{q}}
{% endfor %}

class {{report}}(Report):
    title = "{{report_title}}"
    abbreviate_questions = True
    questions = [
                {% for qn in qnames %}
                ({{qn}}, 10),
                {%- endfor %}
                ]    

    import {{package_name}}
    pack_imports = [{{package_name}}]


if __name__ == "__main__":
    from unitgrade import evaluate_report_student
    evaluate_report_student({{report}}())
"""
        name = self.name
        nname = self.base_name
        report = f"{nname[0].upper()}{nname[1:]}_{self.seed}"
        x = dict(qs=qs, report=report, qnames=qnames, report_title=f"Report for {nname}", package_name=self.package_name)
        s = jinjafy(dirs, fulldoc, x)
        print(s)
        out_complete = f"{dirs.code}/{name}_tests_complete.py"
        with open(out_complete, 'w') as f:
            f.write(s)

        deploy = """
from unitgrade_private import setup_grade_file_report
from snipper import snip_dir
from snipper.load_citations import get_aux, get_bibtex
{{ imporln }}

if __name__ == "__main__":
    setup_grade_file_report({{report}}, remove_hidden=False, bzip=False)
    setup_grade_file_report({{report}}, remove_hidden=True, bzip=False)    
        """
        imporln = f'from {os.path.relpath(out_complete, dirs.base + "/src").replace("/", ".")[:-3]} import {report}'
        x = dict(imporln=imporln, report=report)
        s = jinjafy(dirs, deploy, x)
        deploy_py = f"{dirs.code}/deploy.py"

        with open(deploy_py, 'w') as f:
            f.write(s)
        # Now deploy it.

        c = os.path.relpath( f"{dirs.code}/deploy.py", dirs.base + "/src").replace("/", ".")[:-3]
        src = dirs.base + "/src"
        cmd = f"cd {src} && python -m {c}"
        subprocess.run([cmd], shell=True)
        # Now this has been deployed. Deploy to a student repo.

def jupytext_file(md_file):
    d = os.path.dirname(md_file)
    md_file = os.path.abspath(md_file)
    assert os.path.isfile(md_file)

    cmd = f"cd {os.path.dirname(md_file)} && jupytext --to notebook --set-formats md:myst {os.path.basename(md_file)}"
    o = subprocess.run([cmd], shell=True, capture_output=True)
    print(str(o.stdout.decode("utf8")))

class QuestionController:
    questions = None
    def __init__(self, seed, question_args=None):
        self.seed = seed
        self.question_args = question_args

class Mat1Question(NotebookTestCase, Question):
    notebook = None
    sheet = None

    def __init__(self, *args, seed=None, question_args=None, **kwargs):
        # set up parts of the environment.
        if seed is None:
            seed = 0

        if question_args is None:
            question_args = {}
        Question.__init__(self, seed=seed, question_args=question_args)
        try:
            UTestCase.__init__(self, *args, **kwargs)
        except Exception as e:
            print("Bad init")
            raise e
    def render(self, exam):
        # Use the exam
        self.dirs = exam.get_dirs()
        self.exam = exam
        if not os.path.isdir(self.dirs.generated):
            os.makedirs(self.dirs.generated)
        if not os.path.isdir(self.dirs.figures):
            os.makedirs(self.dirs.figures)

        # Now it is appropriate for the great jinja.
        np.random.seed(self.seed)
        x = self.generate()
        if not isinstance(x, dict):
            x = x.__dict__
        x = {**x, **self._extra_generation(exam)}

        x['overall_exam_score'] = self.overall_exam_score
        x['question_title'] = self.question_title
        x['clearpage'] = self.clearpage
        x['include_solution_box'] = self.include_solution_box

        dn = os.path.basename(os.path.dirname(inspect.getfile(self.__class__)))
        texfile = os.path.dirname(inspect.getfile(self.__class__)) + "/" + os.path.basename(inspect.getfile(self.__class__))[:-3] + ".tex"

        # What should it do?
        # Render the question and return it as a str.
        # from
        s = jinjafy(self.dirs, self.sheet, x)
        return s

    def name(self):
        return f"{self.__class__.__name__}_{self.seed}"

    def render_dummy(self, r):

        class DummyExam(Mat1Exam):
            r = 23
            pass
        ex = DummyExam()
        s = self.render(ex)
        s = JUPYTER_HEAD + "\n\n"+s
        with open("./homework.md", 'w') as f:
            f.write(s.strip())
        # from exam_generator.mat1.mat1exam import jupytext_file
        jupytext_file("./homework.md")
