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


class ExplicitMultipleChoice(MCQuestion):
    def __init__(self, seed, title='', template_base='explicit_question', clearpage=False, **kwargs):
        if template_base.endswith(".tex"):
            raise Exception("Template base should not end with .tex:", template_base)

        super().__init__(seed, title=title, clearpage=clearpage, **kwargs)
        self.template_base = template_base
        # self.bank = bank

    def render(self, exam):
        dirs = exam.get_dirs()

        def chk(path):
            dn = os.path.dirname(dirs.base +"/"+path)
            if not os.path.isdir(dn):
                os.mkdir(dn)
            if not os.path.isfile(dirs.base + "/" + path):
                with open(dirs.base + "/" + path, 'w') as f:
                    if path.endswith("_body.tex"):
                        s = "Which one of the following options are correct?\n"
                        s += """ 
\\iffalse
\\begin{comment} % A should be correct.
\\begin{itemize} 
    \\item Answer A
    \\item Answer B
    \\item Answer C
    \\item Answer D
\\end{itemize}
\\end{comment}
\\fi
\\iffalse
\\begin{solution}
solution here. 
\\end{solution}
\\fi
                            """
                        # elif path.endswith("_answers.tex"):
                        #     s = "\n".join(["\\item Option goes here." for _ in range(4) ])
                    else:
                        s = "Put your solution here."
                    f.write(s)
            # chk(sol)
            return path

        # sol =  chk("static/"+self.template_base +"_sol.tex")
        body = chk("static/"+self.template_base +"_body.tex")

        self.body = body

        return super().render(exam)

    def generate(self):
        x = SimpleNamespace()
        def txt2items(cmd):
            items = None
            if "\\begin{itemize}" in cmd:
                pre = cmd.split("\\begin{itemize}")[0]

                cmd = "x " + cmd.split("\\begin{itemize}")[1]
                cmd = cmd.split("\\end{itemize}")[0]
                items = cmd.split("\\item")[1:]
            else:
                pre = cmd

            return pre, items

        try:
            x.body = self.body
            with open(os.getcwd() + "/" + self.body, 'r') as f:
                ss = f.read()
            if "\\begin{solution}" in ss:
                x.text_solution = ss[ss.find("\\begin{solution}")+len("\\begin{solution}"):ss.find("\\end{solution}")]
                x.text_solution, x.solution_options = txt2items(x.text_solution)
            else:
                x.text_solution = None
                sfile = "static/"+self.template_base +"_body.tex"
                if os.path.isfile(sfile):
                    x.static_solution = sfile
                else:
                    raise Exception("No \\begin{solution} in template and no solution file: "+ sfile)


            cmd = ss.split("\\begin{comment}")[1]
            cmd = "x " + cmd.split("\\begin{itemize}")[1]
            cmd = cmd.split("\\end{itemize}")[0]
            cmd = cmd.split("\\item")[1:]
            if len(cmd) != 4:
                print(ss)
                print("="*100)
                raise Exception("Badly formed answers in: "+ self.body)
            x.answers = [a.strip() for a in cmd]


        except Exception as e:
            print("Bad generation", self.body)
        return x
