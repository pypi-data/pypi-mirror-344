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


class DP01(Mat1Question):
    notebook = 'homework.ipynb'
    sheet = """
## A problem about adding numbers

### a) This problem will surely test your awesome number-adding skills.

In this problem, you should compute $x_1 = a + b$ where $a = {{a}}$ and $b = {{b}}$. 
```{code-cell} ipython3
x1 = None  # Write your result here.
x1 = {{a}} + {{b}} #!b;warn #!b
```

### b) Multiplication

In this problem, you should compute $x_2 = a b$ 
```{code-cell} ipython3
x2 = None  # Write your result here.
x2 = {{a * b}} #!b;warn #!b
```
"""
    def test_addition(self):
        self.assertIsNotNone(self.nb.x1)

    def test_multiplication(self):
        self.assertIsNotNone(self.nb.x2)

    @hide
    def test_addition_hidden(self):
        self.assertEqualC(self.nb.x1)

    @hide
    def test_multiplication_hidden(self):
        self.assertEqualC(self.nb.x2)

    def generate(self):
        x = SimpleNamespace()
        x.a = 1+np.random.randint(100)
        x.b = 1+np.random.randint(100)
        return x

class Arithmetics02(Mat1Question):
    # throw_error_on_no_tex_file = False
    notebook = 'homework.ipynb'
    sheet = """
## A problem about subtracting numbers.

This problem set will test your skills in subtracting numbers

### a) This problem will surely test your awesome number-adding skills.

In this problem, you should compute $x_1 = a + b - c$ where $a = {{a}}$ and $b = {{b}}$ and $c = {{c}}$ 
```{code-cell} ipython3
x1 = None  # Write your result here.
x1 = {{a + b - c}} #!b;warn #!b
print(x1)
```

### b) Multiplication and parenthesis

In this problem, you should compute $x_2 = a (b-c)$ 
```{code-cell} ipython3
x2 = None  # Write your result here.
x2 = {{a * (b-c) }} #!b;warn #!b
print(x2)
```
"""
    def test_addition(self):
        self.assertIsNotNone(self.nb.x1)
        self.assertEqual(self.nb.x_11, 4)

    def test_multiplication(self):
        self.assertIsNotNone(self.nb.x2)

    @hide
    def test_addition_hidden(self):
        self.assertEqualC(self.nb.x1)

    @hide
    def test_multiplication_hidden(self):
        self.assertEqualC(self.nb.x2)

    def generate(self):
        x = SimpleNamespace()
        x.a = 1+np.random.randint(20)
        x.b = 1+np.random.randint(10)
        x.c = 1 + np.random.randint(20)
        return x

class W1Q1Controller(QuestionController):
    questions = [DP01, Arithmetics02]

if __name__ == "__main__":
    q = DP01(seed=3)
    q.render_dummy(r = 3)
    import unittest
    unittest.main()
