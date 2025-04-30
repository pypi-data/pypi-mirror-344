from unitgrade import hide, UTestCase
from exam_generator.exam import Question, jinjafy
from types import SimpleNamespace
import gym
import numpy as np
import sympy as sym
import os
import inspect
from unitgrade import NotebookTestCase
from exam_generator.mat1.mat1exam import Mat1Question
from exam_generator.mat1.mat1exam import QuestionController

class Sympy1(Mat1Question):
    notebook = 'homework.ipynb'
    sheet = """
## A problem with a derivative

### a) This problem will test your awesome differentiation skills.

Consider the function $f(x) = {{latex}}$. What $y_1 = f'({{val}})$? 
```{code-cell} ipython3
y1 = None  # Write your result here.
y1 = {{derivative}} #!b;warn #!b
```
"""
    def test_derivative(self):
        self.assertIsNotNone(self.nb.y1)

    @hide
    def test_derivative_hidden(self):
        self.assertEqualC(self.nb.y1)

    def generate(self):
        x = SimpleNamespace()
        x.a = 1+np.random.randint(4)
        x.b = 1+np.random.randint(2)
        x.val = np.random.randint(5)+2
        import sympy as sym
        z = sym.symbols('x')
        from sympy import latex
        f = x.a * z + z ** x.b
        x.latex = latex(f)
        x.derivative = sym.diff(f, z).subs(z, x.val)
        return x

class Sympy2(Mat1Question):
    notebook = 'homework.ipynb'
    sheet = """
## A problem with more troublesome derivative

### a) Solving an equation involving a derivative

Consider the function $f(x) = {{latex}}$. Suppose that ${{derivative}}= f'({{val}})$, what is $a$?
```{code-cell} ipython3
a = None  # Write your result here.
a = {{a}} #!b;warn #!b
```
"""
    def test_derivative(self):
        self.assertIsNotNone(self.nb.a)

    @hide
    def test_derivative_hidden(self):
        self.assertEqualC(self.nb.a)

    def generate(self):
        d = SimpleNamespace()
        d.a = 3+np.random.randint(6)
        d.b = 2+np.random.randint(10)
        d.val = np.random.randint(5)+2
        import sympy as sym
        x, a = sym.symbols(['x', 'a'])
        from sympy import latex
        f = d.b/a * x**a
        d.latex = latex(f)
        d.derivative = sym.diff(f, x).subs(x, d.val).subs(a, d.a)
        return d




class SymSinCos(Mat1Question):
    notebook = 'homework.ipynb'
    sheet = """
## Derivatives of trigonometric functions

### a) A derivative of the sinus function

Consider the function $f(x) = {{latex}}$. What is $f'({{x0}})$?
```{code-cell} ipython3
q2 = None  # Write your result here.
q2 = {{sol}} #!b;warn #!b
```
"""
    def test_derivative(self):
        self.assertIsNotNone(self.nb.q2)

    @hide
    def test_derivative_hidden(self):
        self.assertEqualC(self.nb.q2)

    def generate(self):
        d = SimpleNamespace()
        d.a = 3+np.random.randint(6)
        d.b = 2+np.random.randint(10)
        d.x0 = np.random.randint(5)+2
        import sympy as sym
        x, a = sym.symbols(['x', 'a'])

        from sympy import latex
        f = sym.sin(d.a * x) * d.b
        d.latex = latex(f)

        # sym.diff(f, x).subs(x, d.x0)

        d.sol = float(sym.diff(f, x).subs(x, d.x0) )

        return d



class W1Q2Controller(QuestionController):
    questions = [Sympy1, Sympy2, SymSinCos]


if __name__ == "__main__":
    q = SymSinCos(seed=3)
    q.render_dummy(r = 3)
