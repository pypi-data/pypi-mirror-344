import setuptools
# py -m build && twine upload dist/*
# Linux> python -m build && python -m twine upload dist/*
# Local install: sudo pip install -e ./

# Manifest candidate:  include src/slider/DTU_Beamer_files/DTU_Beamer_files.zip
setuptools.setup(
    name="exam_generator",
    # packages=find_packages(),
    version="0.0.8",
    description="The DTU Exam generator for programming, conceptual and MC exams.",
    author="Tue Herlau",
    license="See licensing file",
    url='https://lab.compute.dtu.dk/tuhe/dtuexam', # require login; clean repo!
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=["jinja2", "matplotlib", "numpy"],
    include_package_data=True,
    package_data={'': ['templates/*', 'questions/*/*.tex'],},  # Check Manifest.in; required??
)
