from setuptools import setup, find_packages

setup(
    name="dimple_package",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'exp1 = exps.exp1:run',
            'exp2 = exps.exp2:run',
            'exp3 = exps.exp3:run',
            'exp4 = exps.exp4:run',
            'exp5 = exps.exp5:run',
            'exp6 = exps.exp6:run',
            'exp7 = exps.exp7:run',
            'exp8 = exps.exp8:run',
            'exp9 = exps.exp9:run',
            'exp10 = exps.exp10:run',
        ],
    },
)
