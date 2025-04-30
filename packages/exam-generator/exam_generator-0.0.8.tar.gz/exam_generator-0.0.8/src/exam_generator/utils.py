import os, glob, shutil
import sys


def setup_irlc_files(exam):
    # TODO: Parameterize this to make it nicer.
    # Copy files from the irlc folder to the exam irlc folder.
    dirs = exam.get_dirs()
    # sbase = dirs.base + "/../../../02465public/src"
    # sbase = dirs.publ
    sbase = os.path.normpath(dirs.public_git_dir + "/src")
    assert os.path.isdir(sbase)

    dbase =  f"{dirs.base}/src"
    # public_root = os.path.normpath(dirs.base + "/../../../02465public")
    # print(public_root)
    for g in glob.glob(f"{dirs.public_git_dir}/src/irlc/**/*.py", recursive=True):
        srel = os.path.relpath(g, sbase)
        dabs = os.path.normpath(dbase + "/" + srel)
        if not os.path.isdir(os.path.dirname(dabs)):
            os.makedirs(os.path.dirname(dabs))
        # if "lectures" in g:
        #     print(os.path.normpath(g))
        shutil.copy(g, dabs)

def set_irlc_module_destination(irlc):
    # TODO: Parameterize this to make it nicer.

    import inspect
    frame = inspect.stack()[1]
    print("stack", inspect.stack())
    print("frame", frame)
    print("frame[0]", frame[0])
    try:
        module = inspect.getmodule(frame[0])
        _file = module.__file__
        __file__ = _file
        from pathlib import Path
        if Path(__file__).parent not in Path(irlc.__path__[0]).parents:
            sys.path = [p for p in sys.path if os.path.normpath(p) != os.path.dirname(irlc.__path__[0]) ]
            sys.path.append(os.path.dirname(__file__) + "/src")
        import importlib
        print("__file__", __file__)
        importlib.reload(irlc)
        assert Path(__file__).parent in Path(irlc.__path__[0]).parents
    except Exception as e:
        print("Got an exception", e)


