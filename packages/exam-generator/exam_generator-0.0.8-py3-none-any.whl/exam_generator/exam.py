import shutil
import matplotlib.pyplot as plt
import jinja2
from types import SimpleNamespace
import numpy as np
import inspect
import os

class Exam:
    # Functional or OOP? Any difference?
    semester = 'spring'
    questions = []
    output_file = ''
    debug = False
    show_solutions = False
    date = 'March 4th, 2023'
    # centerlabel = 'Midterm test A'
    course_title = "Introduction to reinforcement learning and control"
    header_left = 'Midterm test A'
    header_center = '02465'
    duration = '4 hours'
    midterm = False

    permute_answers = True
    seed = None

    # Used to set package information for paths.
    package_name = 'irlc'
    subpackage_name = 'assignment1'

    @property
    def name(self):
        dirs = self.get_dirs()
        # name = os.path.basename(os.path.dirname(dirs.latex))
        return os.path.basename(dirs.code)

    @property
    def base_name(self):
        return os.path.basename(self._get_base_location())
        # return self.__module__

    def _get_base_location(self):

        print(self.__class__)
        print("Class.get_file(self.__class__", inspect.getfile(self.__class__) )

        gf =  inspect.getfile(self.__class__)
        abs_path = os.path.abspath(gf)
        print("abs_path", abs_path)
        inspect.getfile(self.__class__)
        ff = inspect.getfile(inspect.currentframe())
        print("using crurrent frame", ff)
        print("Using old method", gf)

        if "Exam" in gf:
            gf = gf
        elif "Exam" in abs_path:
            gf = abs_path
        else:
            gf = ff
        print("Returning base dirname from", gf)
        return os.path.dirname(gf)


    @property
    def out_path(self): # Unclear when/where this is used.
        return f"{self.package_name}/{self.subpackage_name}"

    def get_dirs(self):
        dirs = SimpleNamespace()
        base = self._get_base_location()
        print("The base name is", base)
        name = self.base_name
        # base = os.path.dirname(inspect.getfile(self.__class__))
        latex = base + "/latex"
        figures = base + "/latex/figures"

        dirs.base = base
        dirs.latex = latex
        dirs.figures = figures
        dirs.generated = base + "/latex/generated"
        dirs.code = f"{base}/src/{self.package_name}/{self.subpackage_name}/{name}"
        dirs.templates_base = os.path.dirname(inspect.getfile(Exam)) +"/templates"
        dirs.deployment = base + "/deployments"
        import questions as qs
        from exam_generator import questions as qs2

        dirs.templates_bases = [dirs.templates_base] +qs.__path__  + qs2.__path__ #  [os.path.dirname(p) for p in qs.__path__]
        dirs.templates_bases += [dirs.base]


        # This dir should be implemented in a special exam class that inherits from Exam. I do it here because it is simpler but a bit dirty.
        pdir = os.path.normpath(base + "/../../../02465public")
        if not os.path.isdir(pdir):
            pdir =  os.path.normpath(base + "/../../02465public")
            assert os.path.isdir(pdir)

        dirs.public_git_dir = pdir
        dirs.public_git_dir_relative_to_latex = os.path.relpath(dirs.public_git_dir, latex)
        return dirs

    def render(self):
        # If we are doing a deployment, remove the destionation file.

        def bracket(s):
            return "{"+ s+"}"
        # Take each question. Render it to an output directory. Then
        dirs = self.get_dirs()
        ext = '_solutions' if self.show_solutions else ''
        ext += '_noperm' if not self.permute_answers else ''
        file_out = f"{dirs.latex}/{self.name}{ext}.tex"
        deploy_to_pdf = dirs.deployment + "/" + os.path.basename(file_out)[:-4] + ".pdf"
        if os.path.isfile(deploy_to_pdf):
            os.remove(deploy_to_pdf)


        qpath = []

        # This construction is AFAIK not current anymore. Answers seem permuted just fine. Ignoring.
        if self.seed is None:
            pass
            # print("You must set an exam seed to permute the answers")
        np.random.seed(self.seed)

        for sec in self.questions:
            qpath.append(f"\section*{bracket(self.questions[sec]['title'])}")

            for q in self.questions[sec]['questions']:
                print(q)
                # print(q.program_file)
                file = q.render(self)
                path = os.path.relpath(file, dirs.latex)
                path = path.replace("\\", "/")
                qpath.append(f"\input{bracket(path)}")

        pydest = f"{dirs.code}/multiple_choice_answers.py"
        x = {'questions': qpath, 'show_frontpage': True, 'course_title': self.course_title, 'exam_name': self.name, 'date': self.date,
             'midterm_base': os.path.relpath(dirs.code, dirs.base+"/src"),
             'duration': self.duration, 'midterm': self.midterm,
             'header_left': self.header_left,
             'header_center': self.header_center,
             # 'centerlabel': self.centerlabel,
             'show_solutions': self.show_solutions,
             'N_MC': len(self.questions[0]['questions']),
             'mc_answer_path':         os.path.relpath(pydest, dirs.base+"/src"),
             'programming_handin_files': [os.path.relpath(dirs.code, dirs.base+"/src") + "/" + q.program_file for q in self.questions[2]['questions']] ,
             'gradepy': os.path.relpath(dirs.code, dirs.base+"/src") + f'/{self.name}_tests_grade.py',
             'dirs': dirs,
             }

        jinja_write(dirs, template_base="exam_base.tex", x=x, file_out=file_out)
        from slider.latexutils import latexmk
        try:
            pdf_out = file_out[:-4] + ".pdf"
            if os.path.isfile(pdf_out):
                os.remove(pdf_out)
            # Remove the PDF file.
            # print("Compiling latex...")
            latexmk(file_out)
            # print("Compiled.")
            if not self.show_solutions and self.permute_answers:
                # Deployment of exam.
                # pdf_dest = dirs.deployment + "/"+os.path.basename(pdf_out)
                shutil.copyfile(file_out[:-4]+".pdf", deploy_to_pdf)


        except Exception as e:
            with open(file_out[:-4]+".log") as f:
                print(f.read())
            print("Exception caught and handled...")
            raise Exception("The PDF compilation fucked up. I was compiling: ", file_out)


        """ Make answer files for MC questions. """

        # pyans = os.path.dirname(__file__ ) + "/templates/multiple_choice_answers.py"
        # pydest =  f"{dirs.base}/src/{os.path.basename(dirs.base )}/multiple_choice_answers.py"
        x = {'NQ': len(self.questions[0]['questions'])}

        jinja_write(dirs, template_base='multiple_choice_answers.pyt', x=x, file_out=pydest)


def jinja_write(dirs, x, template_base=None, template_str=None, file_out=None):
    templateLoader = jinja2.FileSystemLoader(searchpath=dirs.templates_bases)
    templateLoader = jinja2.FileSystemLoader(searchpath=dirs.templates_bases)

    env = jinja2.Environment(lstrip_blocks=True, trim_blocks=True, loader=templateLoader)
    from exam_generator.jinjaenv import latex_env
    env = latex_env(env)

    if template_base is not None:
        # print(template_base)
        rp = [os.path.relpath(template_base, r) for r in dirs.templates_bases]
        rp = [r for r in rp if not r.startswith("..")]
        if len(rp) == 0:
            rp = [template_base]
        # if len(rp) == 0:
        #     print("Bad! ")
        #     print(template_base, dirs.templates_bases)
        #     assert False
        try:
            template = env.get_template(rp[0])
        except Exception as e:
            print(e)
            raise e
    else:
        template = env.from_string(template_str)
    jinja_out = template.render(x)
    if file_out is not None:
        with open(file_out, 'w', encoding='utf-8') as f:
            f.write(jinja_out)
            # print("Writing to: " + file_out)
    return jinja_out



def jinjafy(dirs, jinja_str, x):
    templateLoader = jinja2.FileSystemLoader(searchpath=dirs.templates_bases)
    env = jinja2.Environment(lstrip_blocks=True, trim_blocks=True, loader=templateLoader)
    from exam_generator.jinjaenv import latex_env
    env = latex_env(env)
    template = env.from_string(jinja_str)
    # template = env.get_template(template_base)
    jinja_out = template.render(x)
    return jinja_out

class Question:
    # template = ''

    dirs = None # set by the exam.
    seed = 3
    _number = 0
    overall_exam_score = 1
    question_title = ''
    include_solution_box = False
    throw_error_on_no_tex_file = True

    template = None

    def __init__(self, seed, *args, title='', clearpage=False, question_args=None):
        self.seed = seed

        self.question_title = title
        self.clearpage = clearpage
        self.question_args = question_args

    def setup(self, args, **kwargs):
        x = SimpleNamespace()
        x.foo = 'bar'
        return x

    def generate(self):
        # Should actually generate the output of this question. This is the method you are supposed to implement.
        raise NotImplementedError("Implement this.")

    def _extra_generation(self, exam):

        return {}

    def render(self, exam):
        # Use the exam
        self.dirs = exam.get_dirs()

        if not os.path.isdir(self.dirs.generated):
            os.makedirs(self.dirs.generated)
        if not os.path.isdir(self.dirs.figures):
            os.makedirs(self.dirs.figures)

        # Now it is appropriate for the great jnja.
        np.random.seed(self.seed)
        self.rng = np.random.default_rng(self.seed)
        # print(self)
        x = self.generate()
        if not isinstance(x, dict):
            x = x.__dict__
        question_args = {} if self.question_args is None else self.question_args

        x = {**question_args, **x, **self._extra_generation(exam)}

        x['overall_exam_score'] = self.overall_exam_score
        x['question_title'] = self.question_title
        x['clearpage'] = self.clearpage
        x['include_solution_box'] = self.include_solution_box

        dn = os.path.basename(os.path.dirname(inspect.getfile(self.__class__)))
        if self.template is None:
            texfile = os.path.dirname(inspect.getfile(self.__class__)) + "/" + os.path.basename(inspect.getfile(self.__class__))[:-3] + ".tex"
            if not os.path.exists(texfile):
                print("> Texfile for question not found:", texfile)
                import glob

                fls = glob.glob(os.path.dirname(texfile) + "/*.tex")
                if len(fls) == 1:
                    print("> Attempting to move alternative texfile in same directory", fls[0])
                    import shutil
                    shutil.move(fls[0], texfile)
                else:
                    if self.throw_error_on_no_tex_file:
                        raise Exception("Texfile not found " + texfile)
                print("Textfile not found", texfile)
            # rtex = os.path.relpath(texfile, self.dirs.templates_bases[1])
            # rtex = rtex.replace("\\", "/")
            texfile = texfile.replace("\\", "/")
        else:
            texfile = None

        file_out = self.dirs.generated + "/" + dn + f"_{Question._number}.tex"
        if os.path.isfile(texfile):
            jinja_write(self.dirs,x=x, template_base=texfile, template_str=self.template, file_out=file_out)
            Question._number += 1
            return file_out
        return None
    def savepdf(self, filename):
        if filename.endswith(".pdf"):
            raise Exception("Please remove the .pdf extension when calling savepdf. Your filename:", filename)

        if not filename.endswith(".pdf"):
            filename += ".pdf"
        filein = self.dirs.latex +"/figures/"+filename
        plt.savefig(self.dirs.latex +"/figures/"+filename, dpi = 250) # default 100.
        from slider.convert import pdfcrop
        pdfcrop(filein, filein)


class ProgrammingQuestion(Question):
    program_file = "PLEAST_SET_PROGRAM_FILE.py"
    include_solution_box = True

    def render(self, exam):
        return super().render(exam)


    def _extra_generation(self, exam):
        dirs = exam.get_dirs()
        with open(dirs.code + "/"+self.program_file, 'r') as f:
            s = f.read()
        lines = s.splitlines()
        x = {}
        for l in lines:
            if l.startswith("def ") and l[5] == "_" and l[4] in 'abcdefg':
                fname = l
                if "->" in fname:
                    fname = fname.split("->")[0].strip() +":"
                x['problem_' + l[4]] = fname[:-1]

        from snipper.snipper_main import censor_file

        if not os.path.isdir(d := dirs.latex + "/output"):
            os.makedirs(d)
        base_path = None # use temp directory.

        f = dirs.code + "/" + self.program_file
        package_base_dir= None #dirs.code
        base_path = os.path.dirname(f)

        nrem, cut = censor_file(f, run_files=False, run_out_dirs=d, cut_files=True,
                                base_path=base_path,
                                references=None,
                                license_head=None,
                                censor_files=False,
                                # package_base_dir=None,
                                package_base_dir=package_base_dir,
                                update_file = False)


        return {'program_file':self.program_file,
                'program_path': os.path.relpath(dirs.code, dirs.base+"/src") + "/"+self.program_file,
                'solution_head': 'The solution can be found in this directory as a \\pyi{.py} file.',
                **x}

class MCQuestion(Question):
    include_solution_box = True

    def __init__(self, *args, answer_permutation=None, **kwargs):
        self.answer_permutation = answer_permutation
        super().__init__(*args, **kwargs)

    def _extra_generation(self, exam):
        # if hasattr(self, 'template_base') and self.template_base == 'bellman': # self.seed == 204:
        #     print("here")
        x = super()._extra_generation(exam)
        if exam.permute_answers:
            # self.set_answer_permutation()
            if self.answer_permutation is not None:
                pass
            else:
                self.answer_permutation = self.rng.permutation(4)
        else:
            self.answer_permutation = (0,1,2,3)

        assert len(self.answer_permutation) == 4
        x['correct_answer'] = 'ABCD'[list(self.answer_permutation).index(0)]

        x['answer_permutation'] = self.answer_permutation
        # print("Using permutation", self.answer_permutation)
        # raise Exception(f"Rng state is {self.rng}")
        return x

    # def set_answer_permutation(self, permutation=None):
    #     # np.random.seed(self.seed)
    #     if permutation is None:
    #         assert False
    #         self.answer_permutation = self.rng.permutation(4)
    #         # print("Using permutation", self.answer_permutation)
    #     else:
    #         self.answer_permutation = permutation