from jinjafy import jinja_env
import numpy as np

def permute_exam_answers(section,permutation):
    permutation = list(permutation)
    if min(permutation) == 1:
        raise Exception(f"the specified permutation is invalid as it does not start with 0. {permutation}")
        # permutation = [i - 1 for i in permutation]
    # permutation.append(len(permutation))

    v = (" x" + section).split("\\item")
    v = v[1:]
    v = [s for s in v if len(s.strip()) > 0]

    if len(v) != len(permutation):
        print(section)
        print("num qs found:", len(v), permutation)
        assert False

    ls = [('\\choice' if p > 0 else '\\CorrectChoice')  + " " + v[p] for k, p in enumerate(permutation)]
    return ' '.join(ls)

def latex_env(env):
    import math
    env.globals['exp'] = math.exp
    env.globals['sqrt'] = math.sqrt
    env.globals['cos'] = math.cos
    env.globals['sin'] = math.sin

    env.globals['mround'] = mround
    env.globals['bold'] = bold
    env.globals['fmat'] = fmat
    env.globals['enumerate'] = enumerate
    env.globals['zip'] = zip
    env.globals['ensure_numpy'] = ensure_numpy
    env.globals['transpose'] = transpose
    import math
    env.globals['ceil'] = math.ceil
    env.globals['floor'] = math.floor


    from pylatexenc import latexencode
    env.globals['utf8tolatex'] = latexencode.utf8tolatex
    env.globals['as_set'] = jinja_env.as_set
    env.globals['as_set_list'] = jinja_env.as_set_list
    env.globals['len'] = jinja_env.mylen
    env.globals['get'] = jinja_env.jget
    env.globals['tolist'] = jinja_env.tolist
    filters = {}

    filters['as_set'] =  as_set
    filters['format_list'] =jinja_env.format_list
    filters['format_join'] = jinja_env.format_join
    filters['format_join_enum'] = jinja_env.format_join_enum
    filters['pm'] = lambda x: f" {x}" if x < 0 else f"+{x}"
    filters['bold'] = bold
    filters['capfirst'] = lambda x: (x[0].upper() + x[1:] if len(x) > 1 else x.upper()) if x != None and isinstance(x, str) else x
    filters['lowerfirst'] = lambda x: (x[0].lower() + x[1:] if len(x) > 1 else x.lower()) if x != None and isinstance(x, str) else x
    filters['infty'] = jinja_env.infty
    filters['n2w'] = jinja_env.n2w
    def latex_url(url):
        if not isinstance(url, str):
            return url
        url = url.replace("%", r"\%")
        return url
    filters['latex_url'] = latex_url
    filters['format_list_symbols'] = jinja_env.format_list_symbols
    filters['mround'] = mround
    def eround(val,l):
        x = str(mround(val, l))
        if l == 0:
            return x
        if '.' not in x:
            x = x + "."
        n = l - (len(x) - x.find(".") - 1)
        if n > 0:
            x = x + "0"*n
        return x

    filters['eround'] = eround
    filters['get'] = jinja_env.jget
    filters['flatten'] = jinja_env.flatten
    filters['aan'] = jinja_env.aan
    filters['bracket'] = bracket
    filters['tolist'] = jinja_env.tolist
    filters['rational'] = jinja_env.as_rational
    filters['permute_exam_answers'] = permute_exam_answers # Use my own for more freedom.
    env.filters.update(filters)

    ### 02465 stuff
    import sympy as sym
    from sympy import Dummy
    def flint(eq):
        """convert floats that are ints to ints"""
        reps = {}
        e = eq.replace(lambda x: x.is_Float and x == int(x), lambda x: reps.setdefault(x, Dummy()))
        return e.xreplace({v: int(k) for k, v in reps.items()})

    env.globals['latex'] = lambda eq: sym.latex(flint(eq))
    return env





def as_set(l):
    if type(l) != list and type(l) != np.ndarray:
        l = [l]
    l = list(l)
    s = [f'{i}' for i in l]
    s = '\{' + ", ".join(s) + "\}"
    return s


def bold(bob,d=True) :
    if not isinstance(bob, str) :
        bob = str(bob)
    if d :
        bob = '\\textbf{' + bob +"}"
    return bob


def fmat(bob,l=2,dobold=False) :
    bob = mround(bob,l)
    bob = bold(bob, dobold)
    return bob

def bracket(s):
    return "{"+str(s)+"}"

def un2str(x, xe, precision=2):
    """pretty print nominal value and uncertainty

        x  - nominal value
        xe - uncertainty
        precision - number of significant digits in uncertainty

        returns shortest string representation of `x +- xe` either as
        x.xx(ee)e+xx
        or as
        xxx.xx(ee)"""
    # base 10 exponents
    x_exp = int(floor(log10(x)))
    xe_exp = int(floor(log10(xe)))

    # uncertainty
    un_exp = xe_exp - precision + 1
    un_int = round(xe * 10 ** (-un_exp))

    # nominal value
    no_exp = un_exp
    no_int = round(x * 10 ** (-no_exp))

    # format - nom(unc)exp
    fieldw = x_exp - no_exp
    fmt = '%%.%df' % fieldw
    result1 = (fmt + '(%.0f)e%d') % (no_int * 10 ** (-fieldw), un_int, x_exp)

    # format - nom(unc)
    fieldw = max(0, -no_exp)
    fmt = '%%.%df' % fieldw
    result2 = (fmt + '(%.0f)') % (no_int * 10 ** no_exp, un_int * 10 ** max(0, un_exp))

    # return shortest representation
    if len(result2) <= len(result1):
        return result2
    else:
        return result1


def mround(val, l=2):
    if not isinstance(l, int):
        return un2str(val, l, 1)
    else:
        if isinstance(val, np.ndarray):
            return np.round(val * 10 ** l) / (10 ** l)
        else:
            return round(val * 10 ** l) / (10 ** l)


def transpose(X):
    return np.transpose( ensure_numpy( X) )


def ensure_numpy(X):
    if type(X) != np.ndarray:
        X = np.asarray(X)
    if X.ndim == 1:
        X = np.transpose( np.expand_dims(X,1) )
    return X
